import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Carbonato Recomendador", layout="wide")

@st.cache_data
def f0(s):
    t = (s*59.88)+278.79
    t = t*1.022*0.000001*50045
    t = int(t)
    return(t)


salinidad = st.sidebar.number_input('Salinidad: ', min_value = 0, 
                                    max_value= 40, value = 20)

recambio = st.sidebar.number_input('% Recambio diario: ', min_value = 0, 
                                    max_value= 15, value=10)

alcalinidad = st.sidebar.number_input('Alcalinidad: ', min_value = 0, 
                                    max_value= 250, value= f0(salinidad))


st.subheader("Aplicación de carbonato")

@st.cache_data
def app_corr(a,r,s):
    r = r/100

    dosis = [float(x)*0.1 for x in range(100,250,50)]
    a_s = f0(s)
    a_obj = a_s*1.6
    


    if a>=a_obj:
        correctivo = pd.DataFrame({
            'kg/ha': 0,
            'dias consec.': np.NaN
        }, index=[0])
    else:
        kgx = []
        lfx = []
        for i in dosis:
            a_rpt = a_obj-(10*(1-r))
            kgx.append(i*10)
            ax = a
            fx=0
            while ax<a_rpt:
                ax = ((ax+i)*(1-r))+(a_s*r)
                fx +=1
            lfx.append(fx)
        correctivo = pd.DataFrame({
            'kg/ha': kgx,
            'dias consec.': lfx
        }, index=range(0,len(dosis)))
    return(correctivo)

correctivo = app_corr(alcalinidad, recambio, salinidad)

@st.cache_data
def app_mant(a,r,s):
    r = r/100

    dosis = 100*0.1
    a_s = f0(s)
    a_obj = a_s*1.6


    if a>=a_obj:
        mantenimiento = pd.DataFrame({
            'kg/ha': dosis*10,
            'frecuencia': 30
        }, index =[0])
    else:
        a_rpt = a_obj-(dosis*(1-r))
        ay = a_rpt+dosis
        fy = 0
        while ay> a_rpt:
            ay = (ay*(1-r))+(a_s*r)
            fy += 1
        mantenimiento = pd.DataFrame({
            'kg/ha' : dosis*10,
            'frecuencia': fy
        }, index=[0])
    return(mantenimiento)

mantenimiento = app_mant(alcalinidad, recambio, salinidad)


col1, col2 = st.columns(2)

with col1:
    st.text('Dosis correctiva')
    st.dataframe(correctivo, hide_index=True)

with col2:
    st.text('Dosis mantenimiento')
    st.dataframe(mantenimiento, hide_index=True)

