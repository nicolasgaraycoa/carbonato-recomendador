import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Parametros", layout="wide")

@st.cache_data
def f0(s):
    t = (s*59.88)+278.79
    t = t*1.02*0.000001*50045
    t = int(t)
    return(t)


salinidad = st.sidebar.number_input('Salinidad: ', min_value = 0, 
                                    max_value= 40, value = 20)

recambio = st.sidebar.number_input('% Recambio diario: ', min_value = 0, 
                                    max_value= 100, value=10)

alcalinidad = st.sidebar.number_input('Alcalinidad: ', min_value = 0, 
                                    max_value= 250, value= f0(salinidad))


st.subheader("Aplicación de carbonato")

@st.cache_data
def reorder(a, r):
    r = r/100
    dif_x = 150-a
    dif_y = 250-a
    ap_x = min(abs(dif_x)*10,100)
    ap_y = min(dif_y*10, 200)
    
    ax = (ap_x/10)+a
    freq_x = 1
    while ax > 110:
        ax = ((1-r)*ax)+(r*a)
        freq_x += 1
    
    ay = (ap_y/10)+a
    freq_y = 1
    while ay > 110:
        ay = ((1-r)*ay)+(r*a)
        freq_y += 1

    resp = pd.DataFrame({
        'rango':['min','max'],
        'dosis/ha': [ap_x, ap_y],
        'frecuencia': [freq_x, freq_y]
    })

    return(resp)


st.write(reorder(alcalinidad, recambio))




