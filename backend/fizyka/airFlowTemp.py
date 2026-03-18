import csv
import pandas as pd
import numpy as np

try:
    from . import profileGenerator as pg
except ImportError:
    # Handle relative import when running as a script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import profileGenerator as pg

class Heater:
    def __init__(self, max_air_flow, max_power, heater_efficiency=1.0, thermal_capacity=70.0):
        self.max_air_flow = max_air_flow  # m3/s
        self.max_power = max_power
        self.heater_efficiency = heater_efficiency
        self.thermal_capacity = thermal_capacity  # J/K
        self.heating_records = None 
    
    def heatingTempRecord(self, length):

        ''' 
        Docstring for temp_record
        
        :param length: number of temperature records to generate
        :return: list of temperature records
        '''
        self.heating_records =  pd.DataFrame({
            "time": range(length),
            "temp_in": [0.0] * length,  # initial temperature
            })
    

        return self.heating_records
    
    def getheating_value(self, time):
        ''' 
        Docstring for getheating_value
        
        :param time: time at which to get the heating value
        :return: heating value at the given time
        '''
        if self.heating_records is None:
            raise ValueError("Heating records not generated. Call heatingTempRecord(length) first.")
        
        if time < 0 or time >= len(self.heating_records):
            raise IndexError("Time index out of range.")
        
        if time in self.heating_records.index:
            return self.heating_records.loc[time, "temp_in"]
        else:
            #interpolate if the time is not in the index
            return np.interp(time, self.heating_records.index, self.heating_records["temp_in"])
    
    def add_heating_value(self, time, temp_in):
        ''' 
        Docstring for add_heating_value
        
        :param time: time at which to add the heating value
        :param temp_in: temperature value to add at the given time
        '''
        if self.heating_records is None:
            raise ValueError("Heating records not generated. Call heatingTempRecord(length) first.")
        
        if time < 0 or time >= len(self.heating_records):
            raise IndexError("Time index out of range.")
        
        self.heating_records.loc[time, "temp_in"] = temp_in

    def calculate_heating_values(self, timelength, fan_speed_curve, heat_power_curve):   
        if self.heating_records is None:
            self.heatingTempRecord(timelength)
        
        self.heating_records.loc[0, "temp_in"] = 225.0
        # self.heating_records.loc[0, "temp_in_static"] = 225.0 

        for time in range(1, timelength):

            fan_speed = fan_speed_curve(time)
            heat_power = heat_power_curve(time)

            # pojemnosc cieplna
            T_prev = self.heating_records.loc[time-1, "temp_in"]
            T_new_dynamic = self.AirTempDynamic(
                T_prev,
                fan_speed,
                heat_power,
                dt=1.0
            )
            self.heating_records.loc[time, "temp_in"] = T_new_dynamic
            
            # # Model bez pojemności cieplnej (statyczny)
            # T_new_static = self.AirTemp(
            #     fan_speed,
            #     heat_power,
            #     temp_normal=25.0
            # )
            # self.heating_records.loc[time, "temp_in_static"] = T_new_static    

    # def AirTemp(self, fan_speed , heat_power,temp_normal = 25, air_density = 1.2, specific_heat = 1005, coeff = 1.0):
    #     ''' 
    #     Docstring for AirTemp 
    #     
    #     :param fan_speed: speed of the fan [0-100%]
    #     :param temp_normal: initial air temperature [°C]
    #     :param heat_power: power of the heater [0-100%]
    #     :param air_density: density of air [kg/m^3]
    #     :param specific_heat: specific heat capacity of air [J/(kg·K)]
    #     :param coeff: coef for adjustment 
    #     '''
    #     air_volume = (fan_speed / 100.0) * self.max_air_flow
    #     heat_power_actual = (heat_power / 100.0) * self.max_power * self.heater_efficiency
    #     return temp_normal + (heat_power_actual * coeff) / (air_density * specific_heat * air_volume)

    def AirTempDynamic(self, T_prev, fan_speed, heat_power,
                   T_in=25.0,
                   air_density=1.2,
                   specific_heat=1005,
                   dt=1.0):

        # przepływ objętościowy (m3/s)
        air_volume = (fan_speed / 100.0) * self.max_air_flow

        # masowy (kg/s)
        m_dot = air_density * air_volume

        # moc grzałki
        heat_power_actual = (heat_power / 100.0) * self.max_power * self.heater_efficiency

        # bilans mocy
        P_cooling = m_dot * specific_heat * (T_prev - T_in)

        dTdt = (heat_power_actual - P_cooling) / self.thermal_capacity

        return T_prev + dt * dTdt


def m3pH_to_m3pS(air_volume_m3pH):
    '''
    Convert air volume from m^3/h to m^3/s
    
    :param air_volume_m3pH: air volume in m^3/h
    :return: air volume in m^3/s
    '''
    return air_volume_m3pH / 3600.0

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    #import profileGenerator
    import csv

    data = pd.read_csv("sym/data/IKAWA/IKAWA 2026-01-23 083241.csv", index_col=False)

    fan_speed = data["fan set"].values
    heat_power = data["heater"].values
    temp_record = data["temp below"].values
    time = data["time"].values
    
    heat_points = []
    fan_points = []
    for i in range(min(len(heat_power), len(fan_speed), len(temp_record))):
        heat_points.append((float(time[i]), float(heat_power[i])))
        fan_points.append((float(time[i]), float(fan_speed[i])))
        
    # print("Heat points:", fan_points)
    heat_points = pg.curveFunction(heat_points)
    fan_points = pg.curveFunction(fan_points)

    heat_func = heat_points.generate_function()
    fan_func = fan_points.generate_function()

    
    print("Fan function at time 50:", fan_func(50))
    
    air_volume = 17  # m^3/h
    air_volume = m3pH_to_m3pS(air_volume)  
    temp_in = 30.0    # *C
    heater_power = 1250.0  # W 
    
    heater = Heater(max_air_flow=air_volume, max_power=heater_power)
    import matplotlib.pyplot as plt
    timelength = len(temp_record)
    heater.calculate_heating_values(timelength, fan_func, heat_func)
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Wykres z pojemnością cieplną
    ax1.plot([x for x in range(timelength)], [heat_func(x) for x in range(timelength)], label="Heat Power (%)", color="red", linestyle="--", linewidth=1)
    ax1.plot([x for x in range(timelength)], [fan_func(x) for x in range(timelength)], label="Fan Speed (%)", color="blue", linestyle="--", linewidth=1)
    ax1.plot(heater.heating_records["time"], heater.heating_records["temp_in"], label="Air Temperature WITH Thermal Capacity (°C)", color="green", linewidth=2.5)
    # ax1.plot(heater.heating_records["time"], heater.heating_records["temp_in_static"], label="Air Temperature WITHOUT Thermal Capacity (°C)", color="purple", linewidth=2.5, linestyle="-.") 
    ax1.plot(time, temp_record*1, label="Recorded Air Temperature (°C)", color="orange", linestyle=":", linewidth=3)
    ax1.legend()
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Temperature (°C) / Control (%)")
    ax1.set_title("Air Temperature Over Time")
    ax1.grid()
    
    # temp_diff = heater.heating_records["temp_in"] - heater.heating_records["temp_in_static"]
    # ax2.plot(heater.heating_records["time"], temp_diff, label="Difference (Dynamic - Static)", color="brown", linewidth=2.5)
    # ax2.axhline(y=0, color="black", linestyle="--", linewidth=1)
    # ax2.legend()
    # ax2.set_xlabel("Time (s)")
    # ax2.set_ylabel("Temperature Difference (°C)")
    # ax2.set_title("Effect of Thermal Capacity")
    # ax2.grid()
    
    plt.tight_layout()
    plt.show()