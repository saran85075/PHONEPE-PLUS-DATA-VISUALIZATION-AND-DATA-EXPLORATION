import streamlit as st
from streamlit_option_menu import option_menu 
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#creating dataframe 

#sql
mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="saran",
                        database="phonepe_data",
                        port="5432")
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

aggre_insurance=pd.DataFrame(table1,columns=("states","years","Quarter","Transcation_type",
                                            "Transcation_count","Transcation_amount"))

#aggre_transcation_df
cursor.execute("SELECT * FROM aggregated_transcation")
mydb.commit()
table2=cursor.fetchall()

aggre_transcation=pd.DataFrame(table2,columns=("states","years","Quarter","Transcation_type",
                                            "Transcation_count","Transcation_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

aggre_user=pd.DataFrame(table3,columns=("states","years","Quarter","Brands",
                                            "Transcation_count","Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("states","years","Quarter","Districts",
                                            "Transcation_count","Transcation_amount"))

#map_transcation_df
cursor.execute("SELECT * FROM map_transcation")
mydb.commit()
table5=cursor.fetchall()

map_transcation=pd.DataFrame(table5,columns=("states","years","Quarter","Districts",
                                            "Transcation_count","Transcation_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("states","years","Quarter","Districts",
                                            "RegisteredUsers","AppOpens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("states","years","Quarter","Pincodes",
                                            "Transcation_count","Transcation_amount"))

#top_transcation_df
cursor.execute("SELECT * FROM top_transcation")
mydb.commit()
table8=cursor.fetchall()

top_transcation=pd.DataFrame(table8,columns=("states","years","Quarter","Pincodes",
                                            "Transcation_count","Transcation_amount"))  

#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("states","years","Quarter","Pincodes",
                                            "RegisteredUsers"))                                          



#transaction year based 
def Transcation_amount_count_Y(df,year):
    sam=df[df["years"] == year]
    sam.reset_index(drop=True,inplace=True)

    samgr=sam.groupby("states")[["Transcation_count","Transcation_amount"]].sum()
    samgr.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(samgr,x="states",y="Transcation_amount",title=f"{year} TRANSCATION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(samgr,x="states",y="Transcation_count",title=f"{year} TRANSCATION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=550,width=50)
        st.plotly_chart(fig_count)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1["features"]:
        state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()

    fig_india_1=px.choropleth(samgr, geojson=data1, locations= "states",featureidkey="properties.ST_NM",
                              color="Transcation_amount", color_continuous_scale="Rainbow",
                              range_color= (samgr["Transcation_amount"].min(),samgr["Transcation_amount"].max()),
                              hover_name= "states",title=f"{year} TRANSCATION AMOUNT", fitbounds= "locations",
                              height=500,width=500)
    fig_india_1.update_geos(visible=False)
    st.plotly_chart(fig_india_1)
    fig_india_2=px.choropleth(samgr, geojson=data1, locations= "states",featureidkey="properties.ST_NM",
                              color="Transcation_count", color_continuous_scale="Rainbow",
                              range_color= (samgr["Transcation_count"].min(),samgr["Transcation_count"].max()),
                              hover_name= "states",title=f"{year} TRANSCATION COUNT", fitbounds= "locations",
                              height=500,width=500)
    fig_india_2.update_geos(visible=False)
    st.plotly_chart(fig_india_2)

    return sam

#transcation quarter based
def Transcation_amount_count_Y_Q(df,quarter):
    sam=df[df["Quarter"] == quarter]
    sam.reset_index(drop=True,inplace=True)

    samgr=sam.groupby("states")[["Transcation_count","Transcation_amount"]].sum()
    samgr.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(samgr,x="states",y="Transcation_amount",title=f"{sam["years"].min()} YEAR {quarter} QUARTER TRANSCATION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count=px.bar(samgr,x="states",y="Transcation_count",title=f"{sam["years"].min()} YEAR {quarter} QUARTER TRANSCATION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=550,width=500)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for feature in data1["features"]:
            state_name.append(feature["properties"]["ST_NM"])

        state_name.sort()
        
        fig_india_1=px.choropleth(samgr, geojson=data1, locations= "states",featureidkey="properties.ST_NM",
                                color="Transcation_amount", color_continuous_scale="Rainbow",
                                range_color= (samgr["Transcation_amount"].min(),samgr["Transcation_amount"].max()),
                                hover_name= "states",title=f"{sam["years"].min()} YEAR {quarter} QUARTER TRANSCATION AMOUNT", fitbounds= "locations",
                                height=500,width=500)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        with col2:
            fig_india_2=px.choropleth(samgr, geojson=data1, locations= "states",featureidkey="properties.ST_NM",
                                    color="Transcation_count", color_continuous_scale="Rainbow",
                                    range_color= (samgr["Transcation_count"].min(),samgr["Transcation_count"].max()),
                                    hover_name= "states",title=f"{sam["years"].min()} YEAR {quarter} QUARTER TRANSCATION COUNT", fitbounds= "locations",
                                    height=500,width=500)
            fig_india_2.update_geos(visible=False)
            st.plotly_chart(fig_india_2)


def aggre_tran_transcation_type(df,state):


    sam=df[df["states"] == state]
    sam.reset_index(drop=True,inplace=True)
    sam=sam.groupby("Transcation_type")[["Transcation_count","Transcation_amount"]].sum()
    sam.reset_index(inplace=True)

    fig_pie_1=px.pie(data_frame=sam,names="Transcation_type",values="Transcation_amount",
                    width=600,title=f"{state.upper()}TRANSCATION AMOUNT",hole=0.4)
    st.plotly_chart(fig_pie_1)

    fig_pie_2=px.pie(data_frame=sam,names="Transcation_type",values="Transcation_count",
                    width=600,title=f"{state.upper()} TRANSCATION COUNT",hole=0.4)
    st.plotly_chart(fig_pie_2)


def aggre_user_plot_1(df, year):
    au=df[df["years"]==year]
    au.reset_index(drop=True, inplace=True)
    aug=pd.DataFrame(au.groupby("Brands")["Transcation_count"].sum())
    aug.reset_index(inplace=True)

    fig_bar_1=px.bar(aug, x="Brands", y="Transcation_count", title= f"{year} BRANDS AND TRANSCATION COUNT",
                    width=800, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return au


##aggre_user_2
def aggre_user_plot_2(df, quarter):
    auq= df[df["Quarter"]==quarter]
    auq.reset_index(drop=True, inplace=True)

    auqg=pd.DataFrame(auq.groupby("Brands")["Transcation_count"].sum())
    auqg.reset_index(inplace=True)

    fig_bar_1=px.bar(auqg, x="Brands", y="Transcation_count", title= f"{quarter} BRANDS AND TRANSCATION COUNT",
                        width=800, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    return auq 

##aggre_user_3
def aggre_user_plot_3(df, state):
    auqs= df[df["states"]==state]
    auqs.reset_index(drop=True, inplace=True)

    fig_bar_1=px.line(auqs, x="Brands", y="Transcation_count", hover_data= "Percentage",
                        title=f"{state.upper()} BRANDS AND TRANSCATION COUNT, PERCENTAGE",width=800, markers= True)
    st.plotly_chart(fig_bar_1)


#map_insurance
def Map_insu_District(df,state):


    sam=df[df["states"] == state]
    sam.reset_index(drop=True,inplace=True)
    sam=sam.groupby("Districts")[["Transcation_count","Transcation_amount"]].sum()
    sam.reset_index(inplace=True)

    fig_bar_1=px.bar(sam, x="Transcation_amount",y="Districts",orientation="h",height=500,
                     title=f"{state.upper()} DISTRICTS AND TRANSCATION AMOUNT",color_discrete_sequence= px.colors.sequential.Mint_r )
    st.plotly_chart(fig_bar_1)

    fig_bar_2=px.bar(sam, x="Transcation_count",y="Districts",orientation="h",height=500,
                     title=f"{state.upper()} DISTRICTS AND TRANSCATION COUNT",color_discrete_sequence= px.colors.sequential.Mint_r )
    st.plotly_chart(fig_bar_2)


#map_insurance_districts
def map_insu_Districts(df,state):


    sam=df[df["states"] == state]
    sam.reset_index(drop=True,inplace=True)
    sam=sam.groupby("Districts")[["Transcation_count","Transcation_amount"]].sum()
    sam.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar( sam, x= "Transcation_amount", y= "Districts", orientation='h',height=600,
                        title= f"{state} DISTRICT AND TRANSCATION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar( sam, x= "Transcation_count", y= "Districts", orientation='h',height=600,
                        title= f"{state} DISTRICT AND TRANSCATION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

#map_user_plot_1

def map_user_plot_1(df,year):
    muy=df[df["years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg= muy.groupby("states")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_bar_1=px.line(muyg, x="states", y=["RegisteredUsers","AppOpens"],
                            title=f"{year} REGISTERED USERS, APPOPENS",width=800,height=800, markers= True)
    st.plotly_chart(fig_bar_1)
    return muy 

#map_user_plot_2
def map_user_plot_2(df,states):
    muys=df[df["states"]=="states"]
    muys.reset_index(drop=True, inplace=True)

    fig_map_user_bar_1=px.bar(muys, x="RegisteredUsers", y="Districts", orientation="h",
                            title= "REGISTERED USER",height=400,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_1) 

    fig_map_user_bar_2=px.bar(muys, x="AppOpens", y="Districts", orientation="h",
                            title= "APPOPENS",height=400,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_bar_2)

#top_insurance_plot1
def top_insurance_plot_1(df,state):
    tiy=df[df["states"]==state]
    tiy.reset_index(drop=True, inplace=True)

    tiyg= tiy.groupby("Pincodes")[["Transcation_count","Transcation_amount"]].sum()
    tiyg.reset_index(inplace=True)

    fig_top_insu_bar_1=px.bar(tiyg, x="Transcation_amount", y="Pincodes", hover_data="Pincodes",
                                title= "TRANSCATION AMOUNT",height=600,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_top_insu_bar_1)
    fig_top_insu_bar_2=px.bar(tiyg, x="Transcation_count", y="Pincodes", hover_data="Pincodes",
                                title= "TRANSCATION COUNT",height=600,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_top_insu_bar_2)

def top_user_plot_1(df,year):
    tuy=df[df["years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["states","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg, x="states", y="RegisteredUsers", color="Quarter", width=900, height=700,
                        color_discrete_sequence= px.colors.sequential.Burgyl,hover_name="states",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)


    return tuy

#sql connection 
def top_chart_transcation_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="saran",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    #plot_1
    query_1=f'''select states,SUM(transcation_amount) AS transcation_amount
                from {table_name}
                GROUP BY states
                ORDER BY transcation_amount DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states","transcation_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="states",y="transcation_amount",title=f"TOP 10 OF TRANSCATION AMOUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
        st.plotly_chart(fig_amount_1)

    #plot_2 
    query_2=f'''select states,SUM(transcation_amount) AS transcation_amount
                from {table_name}
                GROUP BY states
                ORDER BY transcation_amount
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states","transcation_amount"))
    with col2:
        fig_amount_2=px.bar(df_2,x="states",y="transcation_amount",title=f"LAST 10 OF TRANSCATION AMOUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=550,width=500)
        st.plotly_chart(fig_amount_2)

    #plot_3 
    query_3=f'''select states,AVG(transcation_amount) AS transcation_amount
                from {table_name}
                GROUP BY states
                ORDER BY transcation_amount;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states","transcation_amount"))

    fig_amount_3=px.bar(df_3,y="states",x="transcation_amount",title=f"AVERAGE OF TRANSCATION AMOUNT",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=900)
    st.plotly_chart(fig_amount_3)


def top_chart_transcation_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="saran",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    #plot_1
    query_1=f'''select states,SUM(transcation_count) AS transcation_count
                from {table_name}
                GROUP BY states
                ORDER BY transcation_count DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states","transcation_count"))
    col1,col2= st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="states",y="transcation_count",title=f" TOP 10 OF TRANSCATION COUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
        st.plotly_chart(fig_amount_1)

    #plot_2 
    query_2=f'''select states,SUM(transcation_count) AS transcation_count
                from {table_name}
                GROUP BY states
                ORDER BY transcation_count
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states","transcation_count"))
    with col2:
        fig_amount_2=px.bar(df_2,x="states",y="transcation_count",title=f"LAST 10 OF TRANSCATION COUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=550,width=500)
        st.plotly_chart(fig_amount_2)

    #plot_3 
    query_3=f'''select states,AVG(transcation_count) AS transcation_count
                from {table_name}
                GROUP BY states
                ORDER BY transcation_count;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states","transcation_count"))

    fig_amount_3=px.bar(df_3,y="states",x="transcation_count",title=f"AVERAGE OF TRANSCATION COUNT",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=900)
    st.plotly_chart(fig_amount_3)



def top_chart_registered_users(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="saran",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    #plot_1
    query_1=f'''SELECT districts,SUM(registeredusers) AS registeredusers 
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts","registereduser"))
   
    
    fig_amount_1=px.bar(df_1,x="districts",y="registereduser",title=f"TOP 10 OF REGISTERED USER",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
    st.plotly_chart(fig_amount_1)

    #plot_2 
    query_2=f'''SELECT districts,SUM(registeredusers) AS registeredusers 
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10;;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts","registereduser"))

    
    fig_amount_2=px.bar(df_2,x="districts",y="registereduser",title=f"LAST 10 OF REGISTERED USER",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=550,width=500)
    st.plotly_chart(fig_amount_2)

    #plot_3 
    query_3=f'''SELECT districts,AVG(registeredusers) AS registeredusers 
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts","registereduser"))

    fig_amount_3=px.bar(df_3,y="districts",x="registereduser",title=f"AVERAGE OF REGISTERED USER ",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=900)
    st.plotly_chart(fig_amount_3)



def top_chart_appopens(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="saran",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    #plot_1
    query_1=f'''SELECT districts,SUM(appopens) AS appopens 
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts","appopens"))

    fig_amount_1=px.bar(df_1,x="districts",y="appopens",title=f"TOP 10 OF APPOPENS",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
    st.plotly_chart(fig_amount_1)

    #plot_2 
    query_2=f'''SELECT districts,SUM(appopens) AS appopens
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts","appopens"))

    fig_amount_2=px.bar(df_2,x="districts",y="appopens",title=f"LAST 10 OF APPOPENS",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=550,width=500)
    st.plotly_chart(fig_amount_2)

    #plot_3 
    query_3=f'''SELECT districts,AVG(appopens) AS appopens 
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts","appopens"))

    fig_amount_3=px.bar(df_3,y="districts",x="appopens",title=f"AVERAGE OF APPOPENS ",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=900)
    st.plotly_chart(fig_amount_3)



def top_chart_registered_userss(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="saran",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    #plot_1
    query_1=f'''SELECT states, SUM(registeredusers) AS registeredusers
                from {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states","registereduserss"))

    fig_amount_1=px.bar(df_1,x="states",y="registereduserss",title=f"TOP 10 OF REGISTERED USERSS",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=550,width=500)
    st.plotly_chart(fig_amount_1)

    #plot_2 
    query_2=f'''SELECT states, SUM(registeredusers) AS registeredusers
                from {table_name}
                GROUP BY states
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states","registereduserss"))

    fig_amount_2=px.bar(df_2,x="states",y="registereduserss",title=f"LAST 10 OF REGISTERED USERSS",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=550,width=500)
    st.plotly_chart(fig_amount_2)

    #plot_3 
    query_3=f'''SELECT states, AVG(registeredusers) AS registeredusers
                from {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states","registereduserss"))

    fig_amount_3=px.bar(df_3,y="states",x="registereduserss",title=f"AVERAGE OF REGISTERED USERSS ",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=700,width=900)
    st.plotly_chart(fig_amount_3)


   
#streamlit part 

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    
    select=option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        with col2:
                st.image(Image.open(r"C:/Users/kumar/OneDrive/Desktop/phone_pe/images.jpeg"),width=450)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:/Users/kumar/OneDrive/Desktop/phone_pe/phonepe-upi-lite1683122560381.jpg"))

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\kumar\OneDrive\Desktop\phone_pe\1676025622-news.jpeg"))

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 =st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method=st.radio("Select the Method",["Insurance Analysis","Transcation Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2=st.columns(2)
            with col1:

             years=st.slider("Select The Year",aggre_insurance["years"].min(),aggre_insurance["years"].max(),aggre_insurance["years"].min())
            sa_m=Transcation_amount_count_Y(aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:

             quarters=st.slider("Select The Quarters",sa_m["Quarter"].min(),sa_m["Quarter"].max(),sa_m["Quarter"].min())
             Transcation_amount_count_Y_Q(sa_m,quarters)

        elif method == "Transcation Analysis":

            col1,col2=st.columns(2)
            with col1:

             years=st.slider("Select The Year",aggre_transcation["years"].min(),aggre_transcation["years"].max(),aggre_transcation["years"].min())
            aggre_sam=Transcation_amount_count_Y(aggre_transcation,years)

            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The state", aggre_sam['states'].unique())
             aggre_tran_transcation_type(aggre_sam,states)


        elif method == "User Analysis":
            years=st.slider("Select The Year",aggre_user["years"].min(),aggre_user["years"].max(),aggre_user["years"].min())
            aggre_user_y=aggre_user_plot_1(aggre_user,years)

            quarters=st.slider("Select The Quarters",aggre_user_y["Quarter"].min(),aggre_user_y["Quarter"].max(),aggre_user_y["Quarter"].min())
            aggre_user_y_q=aggre_user_plot_2(aggre_user_y,quarters)

            states=st.selectbox( "Select The state", aggre_user_y_q['states'].unique())
            aggre_user_plot_3(aggre_user_y_q,states)



    with tab2:

        method_2=st.radio("Select the Method",["Map Insurance","Map Transcation","Map User"])

        if method_2== "Map Insurance":
            col1,col2=st.columns(2)
            with col1:
             years=st.slider("Select The Year",map_insurance["years"].min(),map_insurance["years"].max(),map_insurance["years"].min(),key="6")
            Map_insu_tac_Y=Transcation_amount_count_Y(map_insurance, years)

            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The state_mi", Map_insu_tac_Y['states'].unique())
             map_insu_Districts(Map_insu_tac_Y,states)

             
        elif method == "Map Transcation":
            col1,col2=st.columns(2)
            with col1:
             years=st.slider("Select The Year",map_transcation["years"].min(),map_transcation["years"].max(),map_transcation["years"].min(),key="6")
            map_trans_y=Transcation_amount_count_Y(map_transcation, years)

            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The State_mi", map_trans_y['states'].unique())
             map_insu_Districts(map_trans_y,states)


        elif method == "Map User":
            col1,col2=st.columns(2)
            with col1:
             years=st.slider("Select The Year",map_user["years"].min(),map_user["years"].max(),map_user["years"].min(),key="6")
            map_user_y=map_user_plot_1(map_user, years)
            
            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The State_mu", map_user_y['states'].unique())
             map_user_plot_2(map_user_y,states)

 
    with tab3:

        method_3=st.radio("Select the Method",["Top Insurance","Top Transcation","Top User"])

        if method_3== "Top Insurance":

            col1,col2=st.columns(2)
            with col1:
             years=st.slider("Select The Year",top_insurance["years"].min(),top_insurance["years"].max(),top_insurance["years"].min(),key="7")
            top_insu_y=Transcation_amount_count_Y(top_insurance, years)

            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The State_ti", top_insu_y['states'].unique())
             top_insurance_plot_1(top_insu_y,states)


        elif method_3 == "Top Transcation":
            col1,col2=st.columns(2)
            with col1:
             years=st.slider("Select The Year",top_transcation["years"].min(),top_transcation["years"].max(),top_transcation["years"].min(),key="8")
            top_trans_y=Transcation_amount_count_Y(top_transcation, years)

            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The State_tt", top_trans_y['states'].unique())
             top_insurance_plot_1(top_trans_y,states)
        
        
        elif method_3 == "Top User":
            col1,col2=st.columns(2)
            with col1:
             years=st.slider("Select The Year",top_user["years"].min(),top_user["years"].max(),top_user["years"].min(),key="9")
            top_user_y=top_user_plot_1(top_user, years)

            col1,col2=st.columns(2)
            with col1:
                
             states=st.selectbox( "Select The State_tt", top_user_y['states'].unique())
             top_insurance_plot_1(top_user_y, states)

elif select == "TOP CHARTS":
    question=st.selectbox("Select the Question",["1. Transcation Amount and Count of Aggregated Insurance",
                                                 "2. Transcation Amount and Count of Map Insurance",
                                                 "3. Transcation Amount and Count of Top Insurance",
                                                 "4. Transcation Amount and Count of Aggregated Transcation",
                                                 "5. Transcation Amount and Count of Map Transcation",
                                                 "6. Transcation Amount and Count of Top Transcation",
                                                 "7. Transcation count of Aggregated User",
                                                 "8. Registered users of Map User",
                                                 "9. App opens of Map user",
                                                 "10. Registered users of Top User",
                                                 ])
    if question=="1. Transcation Amount and Count of Aggregated Insurance":
       
       st.subheader("TRANSCATION AMOUNT")
       top_chart_transcation_amount("aggregated_insurance")

       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("aggregated_insurance")

    elif question=="2. Transcation Amount and Count of Map Insurance":
       
       st.subheader("TRANSCATION AMOUNT")
       top_chart_transcation_amount("map_insurance")

       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("map_insurance")

    elif question=="3. Transcation Amount and Count of Top Insurance":
       
       st.subheader("TRANSCATION AMOUNT")
       top_chart_transcation_amount("top_insurance")

       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("top_insurance")

    elif question=="4. Transcation Amount and Count of Aggregated Transcation":
       
       st.subheader("TRANSCATION AMOUNT")
       top_chart_transcation_amount("aggregated_transcation")

       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("aggregated_transcation")

    elif question=="5. Transcation Amount and Count of Map Transcation":
       
       st.subheader("TRANSCATION AMOUNT")
       top_chart_transcation_amount("map_transcation")

       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("map_transcation")

    elif question=="6. Transcation Amount and Count of Top Transcation":
       
       st.subheader("TRANSCATION AMOUNT")
       top_chart_transcation_amount("top_transcation")

       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("top_transcation")

    elif question=="7. Transcation count of Aggregated User":
       
       st.subheader("TRANSCATION COUNT")
       top_chart_transcation_count("aggregated_user")

    elif question=="8. Registered users of Map User":
       
       states= st.selectbox("select the state",map_user["states"].unique())
       st.subheader("REGISTERED USERS")
       top_chart_registered_users("map_user",states)

    elif question=="9. App opens of Map user":
       
       states= st.selectbox("select the state",map_user["states"].unique())
       st.subheader("APPOPENS")
       top_chart_appopens("map_user",states)

    elif question=="10. Registered users of Top User":
       
       st.subheader("REGISTERED USERSS")
       top_chart_registered_userss("top_user")
    
       



