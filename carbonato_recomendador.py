import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Carbonato Recomendador", layout="wide")

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
    dosis = range(50,200,50)

    fmax = []

    for i in dosis:
        i = int(i)
        ax = (i/10)+a
        freq = 0
        if a>=180:
            fmax.append(30)
        elif ax>180:
            while ax>180:
                ax = ((1-r)*ax)+(r*a)
                freq += 1
            fmax.append(freq)
        else:
            fmax.append(0)

    
    fmin = []
    
    for i in dosis:
        i = int(i)
        ax = (i/10)+a
        freq = 0
        if a>=130 :
            fmin.append(30)
        elif ax>130:
            while ax>130:
                ax = ((1-r)*ax)+(r*a)
                freq += 1
            fmin.append(freq)
        else:
            fmin.append(0)


    resp = pd.DataFrame({
        'dosis/ha': dosis,
        'frecuencia_baja': fmin,
        'frecuencia_alta': fmax
    })

    return(resp)


st.write(reorder(alcalinidad, recambio))
