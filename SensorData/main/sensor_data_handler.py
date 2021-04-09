from .utils import *

class SensorDataHandler:
    _time_field = None
    _reading_field = None
    _status_field = None
    _sensor_field = None
    _data_frame = None

    def __init__(self, csv_file, time_field, reading_field, status_field, sensor_field):
        self._data_frame = pd.read_csv(csv_file)
        self._time_field = time_field
        self._reading_field = reading_field
        self._status_field = status_field
        self._sensor_field = sensor_field

    def apply(self, method="summarise", status="ON"):
        #Extract data w.r.t. the input status
        acceptable_entries = self._data_frame[self._status_field] == status
        acceptable_data = self._data_frame.where(acceptable_entries)
        grouped_data = acceptable_data.groupby([self._sensor_field])
        neighbourhood_size = 5

        if method == "max":
            return grouped_data.apply(maximum, self._time_field)
        elif method == "min":
            return grouped_data.apply(minimum, self._time_field)
        elif method == "maxima_count":
            return grouped_data.apply(maxima_count, (self._time_field, neighbourhood_size))
        elif method == "minima_count":
            return grouped_data.apply(minima_count, (self._time_field, neighbourhood_size))
        elif method == "calc_slopes":
            return grouped_data.apply(calc_slopes, (self._time_field, self._reading_field))
        elif method == "summarise":
            return grouped_data.apply(summarise, (self._time_field, self._reading_field, self._sensor_field, neighbourhood_size))
        else:
            print("{0} is not a registered method".format(method))
            return None

    def __str__(self):
         return '''
Fields:
-------
Time field : {0}
Reading field : {1}
Sensor Field : {2}
Status Field : {3}

Data frame :
-----------
{4}

Grouped Data :
--------------
{5}
     '''.format(self._time_field, self._reading_field, self._sensor_field, self._status_field, self._data_frame, self.grouped_data.groups.keys())
