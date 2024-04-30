import pandas as pd

class DataDiagnoser:
    def __init__(self, dataframe, first_columns=None, last_columns=None, ignore_columns=None):
        """
        Inicializa la clase DataDiagnoser con un DataFrame de Pandas y los criterios de ordenación de columnas.
        
        Args:
        dataframe (pandas.DataFrame): El DataFrame de Pandas que se utilizará para el diagnóstico.
        first_columns (list): Lista de nombres de columnas que se colocarán al principio del DataFrame.
        last_columns (list): Lista de nombres de columnas que se colocarán al final del DataFrame.
        ignore_columns (list): Lista de nombres de columnas que se ignorarán durante el diagnóstico.
        """
        self.dataframe = dataframe
        self.first_columns = first_columns if first_columns else []
        self.last_columns = last_columns if last_columns else []
        self.ignore_columns = ignore_columns if ignore_columns else []

        # Ordenar el DataFrame al inicializar la clase
        self.sorted_dataframe = self._sort_dataframe()

    def _sort_dataframe(self):
        """
        Ordena las columnas del DataFrame según los criterios especificados.
        
        Returns:
        pandas.DataFrame: El DataFrame con las columnas ordenadas según los criterios especificados.
        """
        all_columns = list(self.dataframe.columns)
        remaining_columns = [col for col in all_columns if col not in self.first_columns + self.last_columns]

        sorted_columns = self.first_columns + remaining_columns + self.last_columns
        sorted_dataframe = self.dataframe[sorted_columns]

        return sorted_dataframe

    def diagnose_missing_values(self):
        """
        Identifica y cuenta los valores faltantes en cada columna del DataFrame.
        
        Returns:
        pandas.DataFrame: Un DataFrame que contiene la frecuencia absoluta y porcentual de valores faltantes en cada columna.
        """
        # Filtrar las columnas a ignorar
        df_to_diagnose = self.sorted_dataframe.drop(columns=self.ignore_columns)
        
        missing_values_abs = df_to_diagnose.isnull().sum()
        missing_values_pct = (missing_values_abs / len(df_to_diagnose)) * 100
        
        # Crear un DataFrame con las frecuencias absolutas y porcentuales
        missing_values_df = pd.DataFrame({
            'Missing Values Absolute': missing_values_abs,
            'Missing Values Percentage': missing_values_pct
        })
        
        return missing_values_df

    def diagnose_data_types(self):
        """
        Determina el tipo de datos de cada columna del DataFrame.
        
        Returns:
        pandas.Series: Una Serie donde el índice son los nombres de las columnas y los valores son los tipos de datos correspondientes.
        """
        # Filtrar las columnas a ignorar
        df_to_diagnose = self.sorted_dataframe.drop(columns=self.ignore_columns)
        
        data_types = df_to_diagnose.dtypes
        return data_types
    
    def diagnose_unique_values(self):
        """
        Cuenta los valores únicos en cada columna del DataFrame y calcula el porcentaje de valores únicos respecto al total de registros.
        
        Returns:
        pandas.DataFrame: Un DataFrame que contiene la cantidad de valores únicos y el porcentaje de valores únicos en cada columna.
        """
        # Filtrar las columnas a ignorar
        df_to_diagnose = self.sorted_dataframe.drop(columns=self.ignore_columns)
        
        unique_values_count = df_to_diagnose.nunique()
        unique_values_pct = (unique_values_count / len(df_to_diagnose)) * 100
        
        # Crear un DataFrame con las cantidades y porcentajes de valores únicos
        unique_values_df = pd.DataFrame({
            'Unique Values Count': unique_values_count,
            'Unique Values Percentage': unique_values_pct
        })
        
        return unique_values_df

    def diagnose_min_max_values(self):
        """
        Calcula el valor mínimo y máximo en cada columna del DataFrame, si la columna es numérica.
        Si la columna no es numérica, decide qué información adicional sería más útil.
        
        Returns:
        pandas.DataFrame: Un DataFrame que contiene el valor mínimo y máximo en cada columna numérica.
        """
        # Filtrar las columnas a ignorar
        df_to_diagnose = self.sorted_dataframe.drop(columns=self.ignore_columns)
        
        min_max_values = {}
        for column in df_to_diagnose.columns:
            if pd.api.types.is_numeric_dtype(df_to_diagnose[column]):
                min_value = df_to_diagnose[column].min()
                max_value = df_to_diagnose[column].max()
                min_max_values[column] = {'Min': min_value, 'Max': max_value}
            else:
                # Si la columna no es numérica, decide qué información adicional sería más útil.
                min_max_values[column] = 'Not numeric'
        
        # Crear un DataFrame con los valores mínimos y máximos
        min_max_values_df = pd.DataFrame(min_max_values).T
        
        return min_max_values_df

    def diagnose(self):
        """
        Combina los resultados de los diagnósticos en un solo DataFrame.
        
        Returns:
        pandas.DataFrame: Un DataFrame que contiene los resultados de los diagnósticos.
        """
        data_types = self.diagnose_data_types().to_frame(name='Data Types')
        missing_values = self.diagnose_missing_values()
        unique_values = self.diagnose_unique_values()
        min_max_values = self.diagnose_min_max_values()
        # Aquí puedes agregar más resultados de diagnóstico según sea necesario
        
        combined_results = pd.concat([data_types, missing_values, unique_values, min_max_values], axis=1)
        return combined_results