import json
import numpy as np
import pandas as pd
from datetime import datetime, timezone


class Simulator:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=["user_id", "timestamp", "heart_rate", "respiration_rate", "activity"]
        ).astype(int)
        self.stats_df_columns = [
            "user_id", "seg_start", "seg_end", "avg_hr", "max_hr", "min_hr", "avg_rr", "max_rr", "min_rr",
            "avg_activity", "max_activity", "min_activity"
        ]
        self.output_df = self.hourly_res_df = pd.DataFrame(
            columns=self.stats_df_columns
        )
        self.type_conv_mapping = {
            "user_id": int, "seg_start": int, "seg_end": int,
            "max_hr": int, "min_hr": int, "max_rr": int, "min_rr": int,
            "max_activity": int, "min_activity": int
        }

    @staticmethod
    def get_sensor_data(time: int):
        """
        Generate random data for heart rate, respiration rate, activity
        :param time: int - the timestamp to be stored against the data
        :return: dict - sensor data for that particular timestamp
        """
        return dict(
            user_id=1,
            timestamp=time,
            heart_rate=np.random.randint(30, 180),
            respiration_rate=np.random.randint(8, 40),
            activity=np.random.randint(0, 100)
        )

    def process_data(self, data: dict):
        """
        Processor function - processes all the sensor data to generate stats every 15 mins
        :param data: dict - Second-wise sensor data
        """
        self.df = self.df.append(data, ignore_index=True)
        if len(self.df) and len(self.df) % (60 * 15) == 0:
            last_15_mins_df = self.df.tail(60 * 15).reset_index(drop=True)
            new_res_row = dict(
                user_id=last_15_mins_df["user_id"][0],
                seg_start=last_15_mins_df["timestamp"][0],
                seg_end=last_15_mins_df["timestamp"][60 * 15 - 1],
                avg_hr=last_15_mins_df["heart_rate"].mean(),
                max_hr=last_15_mins_df["heart_rate"].max(),
                min_hr=last_15_mins_df["heart_rate"].min(),
                avg_rr=last_15_mins_df["respiration_rate"].mean(),
                max_rr=last_15_mins_df["respiration_rate"].max(),
                min_rr=last_15_mins_df["respiration_rate"].min(),
                avg_activity=last_15_mins_df["activity"].mean(),
                max_activity=last_15_mins_df["activity"].max(),
                min_activity=last_15_mins_df["activity"].min(),
            )
            self.output_df = self.output_df.append(new_res_row, ignore_index=True)

    def process_for_hourly(self, segment_df: pd.DataFrame):
        """
        (For Optional functionality)
        Processes 15 min dataframe and returns hourly data
        :param segment_df: pd.DataFrame - will contain avg, min, max sensor data for every 15 mins
        """
        i = 0
        while i < len(segment_df):
            last_hour_df = segment_df.iloc[i:60//15+i].reset_index(drop=True)
            new_res_row = dict(
                user_id=last_hour_df["user_id"][0],
                seg_start=last_hour_df["seg_start"][0],
                seg_end=last_hour_df["seg_end"][60//15-1],
                avg_hr=last_hour_df["avg_hr"].mean(),
                max_hr=last_hour_df["max_hr"].max(),
                min_hr=last_hour_df["min_hr"].min(),
                avg_rr=last_hour_df["avg_rr"].mean(),
                max_rr=last_hour_df["max_rr"].max(),
                min_rr=last_hour_df["min_rr"].min(),
                avg_activity=last_hour_df["avg_activity"].mean(),
                max_activity=last_hour_df["max_activity"].max(),
                min_activity=last_hour_df["min_activity"].min(),
            )
            self.hourly_res_df = self.hourly_res_df.append(new_res_row, ignore_index=True)
            i += 60//15

    @staticmethod
    def round_decimal_points(df: pd.DataFrame):
        """
        Rounding off decimal places to 2 for float columns
        :param df: pd.DataFrame
        :return: pd.DataFrame
        """
        for col in df.columns:
            if "float" in str(df[col].dtype):
                df[col] = df[col].round(2)
        return df

    def run_simulation(self, duration):
        """
        Main function to run the simulation
        :param duration: int - duration to run the simulation for (in seconds)
        """
        # set initial time as the start of the utc hour
        initial_time = datetime.now(tz=timezone.utc)
        initial_time = int(initial_time.replace(tzinfo=timezone.utc, minute=0, second=0, microsecond=0).timestamp())

        # running simulation
        for i in range(duration):
            data = self.get_sensor_data(initial_time + i)
            self.process_data(data)

        # Optional task
        self.process_for_hourly(self.output_df)

        # Post Processing
        self.output_df = self.output_df.astype(self.type_conv_mapping)
        self.output_df = self.round_decimal_points(self.output_df)

        self.hourly_res_df = self.hourly_res_df.astype(self.type_conv_mapping)
        self.hourly_res_df = self.round_decimal_points(self.hourly_res_df)

        # Saving data locally
        with open("input.json", "w") as jf:
            json.dump(self.df.to_dict(orient="records"), jf, indent=2)

        self.output_df.to_csv("output.csv", index=False)
        self.hourly_res_df.to_csv("hourly_stats.csv", index=False)


if __name__ == "__main__":
    Simulator().run_simulation(duration=2*60*60)
