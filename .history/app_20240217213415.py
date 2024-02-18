import streamlit as st
import pandas as pd

# Cambia 'ruta/al/archivo.csv' por la ruta real de tu archivo CSV
df_salario = pd.read_csv('carreras_Salario_Final.csv')

def calcular_retorno_inversion(row, inflacion=0.05, porcentaje_ahorro=0.30):
        salario_anual_disponible = (row['MEDIANA_SALARIO'] * 12) * porcentaje_ahorro
        if pd.notnull(salario_anual_disponible) and pd.notnull(row['costo_total_con_inflacion']):
            retorno_anos = row['costo_total_con_inflacion'] / (salario_anual_disponible * (1 + inflacion)**4)
            return retorno_anos
        else:
            return None

# Título y configuración de la barra lateral
# Título y configuración de la barra lateral

st.image( 'appLogo.png' ,width=200)
st.header("Encuentra la carrera que se ajusta a tu presupuesto y conoce -en tiempo y dinero- el retorno de tu inversión👨‍🏫")
st.divider()

# has una calculadora que reciba el numero de semetre y la inversion aproximada por semestre

st.subheader("Ingresa el número de semestres que durará tu carrera")
semestres = st.number_input('Número de semestres', value=10, step=1)
inversion_semestre = st.number_input('Inversión estimada por semestre', value=4000000, step=100000)
inversion_total = semestres * inversion_semestre
st.markdown(f" ### **Tu inversión total será de**: {inversion_total:,.0f}COP")

st.divider()

st.subheader("Ingresa el rango de tu inversión para toda tu educación superior")
min_inversion = st.number_input('Mínimo de Inversión para toda tu carrera', value=82000000, step=1000000)
# Mostrar min_inversion y max_inversion con formato
st.markdown(f"**Mínimo de inversión para toda tu carrera**: {min_inversion:,.0f} COP")

max_inversion = st.number_input('Máximo de Inversión para toda tu carrera', value=90000000, step=1000000)
st.markdown(f"**Máximo de inversión para toda tu carrera**: {max_inversion:,.0f} COP")

# Selector de categoría con opción para "Todas las Categorías"
categorias = df_salario['CINE_F_2013_AC_CAMPO_DETALLADO'].unique().tolist()
categorias.sort()  # Opcional: Ordenar las categorías alfabéticamente
categorias = ['Todas las Categorías'] + categorias  # Añadir opción para no filtrar
categoria_seleccionada = st.selectbox('Selecciona tu área de interés educativa', categorias)

# Botón de calcular
boton_calcular = st.button('Calcular')


# Título principal y subtítulo en el área de contenido principal


st.divider()

# Lógica para filtrar y calcular el retorno de inversión
if boton_calcular:
    df_filtrado = df_salario if categoria_seleccionada == 'Todas las Categorías' else df_salario[df_salario['CINE_F_2013_AC_CAMPO_DETALLADO'] == categoria_seleccionada]
    carreras_filtradas = df_filtrado[(df_filtrado['costo_total_con_inflacion'] >= min_inversion) & (df_filtrado['costo_total_con_inflacion'] <= max_inversion)].copy()
    carreras_filtradas['años_retorno_inversion'] = carreras_filtradas.apply(calcular_retorno_inversion, axis=1)
    carreras_filtradas.dropna(subset=['años_retorno_inversion'], inplace=True)
    top_3_carreras = carreras_filtradas.sort_values('años_retorno_inversion', ascending=True).head(3)
    
    if top_3_carreras.empty:
        st.warning("Ups, tal vez debes incrementar o disminuir tu inversión mínima.")
    else:
    
        # Asegurarse de seleccionar solo las columnas deseadas
        columnas_deseadas = ['NOMBRE_DEL_PROGRAMA', 'años_retorno_inversion', 'costo_total_con_inflacion', 'MEDIANA_SALARIO']
        tabla_top_3 = top_3_carreras[columnas_deseadas]
        tabla_top_3_styled = tabla_top_3.style.format({
            'Años para Retorno de Inversión': '{:.2f} años',
            'Costo total de la carrera': '${:,.2f}',
            'Mediana de salario': '${:,.2f}'
        })
        
        # Mostrar la tabla estilizada en Streamlit
        st.dataframe(tabla_top_3_styled)
