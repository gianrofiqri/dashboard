import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Universitas - Analisis Program Studi",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Data mahasiswa.csv')
        df.columns = df.columns.str.strip()
        df['Status_Lulus'] = df['Lulus pada Prodi'].apply(
            lambda x: 'Lulus' if (pd.notna(x) and str(x).strip() != 'Tidak Lulus') else 'Tidak Lulus'
        )
        df = df.dropna(subset=['Pilihan 1'])
        df['JK'] = df['JK'].astype(str).str.strip()
        df['bidikmisi'] = df['bidikmisi'].astype(str).str.strip()
        df['Pilihan 1'] = df['Pilihan 1'].astype(str).str.strip()
        return df
    except:
        st.error("File 'Data mahasiswa.csv' tidak ditemukan!")
        return None

def apply_filters(df, jk_filter, bidikmisi_filter):
    filtered_df = df.copy()
    if jk_filter != 'Semua':
        jk_mapping = {'Laki-laki': 'L', 'Perempuan': 'P'}
        filtered_df = filtered_df[filtered_df['JK'] == jk_mapping.get(jk_filter, jk_filter)]
    if bidikmisi_filter != 'Semua':
        filtered_df = filtered_df[filtered_df['bidikmisi'] == bidikmisi_filter]
    return filtered_df

def create_popularity_chart(data):
    all_prodi = data['Pilihan 1'].value_counts()
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    fig = px.pie(
        values=all_prodi.values,
        names=all_prodi.index,
        title=f"<b>Distribusi Semua Program Studi ({len(all_prodi)} Program Studi)</b>",
        color_discrete_sequence=colors[:len(all_prodi)]
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=9,
        pull=0,
        hovertemplate='<b>Prodi:</b> %{label}<br><b>Mahasiswa:</b> %{value}<extra></extra>'
    )
    
    fig.update_layout(
        height=550,
        title_font_size=16,
        title_x=0.5,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01, font=dict(size=8)),
        margin=dict(l=50, r=200, t=60, b=50),
        template="plotly_white"
    )
    
    return fig, all_prodi

def create_graduation_chart(data, all_prodi_names):
    df_all_prodi = data[data['Pilihan 1'].isin(all_prodi_names)]
    prodi_lulus_crosstab = pd.crosstab(df_all_prodi['Pilihan 1'], df_all_prodi['Status_Lulus'], normalize='index') * 100
    prodi_lulus_crosstab = prodi_lulus_crosstab.reindex(all_prodi_names)
    
    fig = go.Figure()
    chart_height = max(600, min(1200, len(all_prodi_names) * 30))
    colors = {'Lulus': '#28a745', 'Tidak Lulus': '#dc3545'}
    
    for status in prodi_lulus_crosstab.columns:
        fig.add_trace(go.Bar(
            name=status,
            x=prodi_lulus_crosstab.index,
            y=prodi_lulus_crosstab[status],
            marker_color=colors.get(status, '#6c757d'),
            text=[f'{val:.1f}%' for val in prodi_lulus_crosstab[status]],
            textposition='inside',
            textfont=dict(color='white', size=8, family="Arial Black"),
            hovertemplate='<b>Prodi:</b> %{x}<br><b>Status:</b> ' + status + '<br><b>Persentase:</b> %{y:.1f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title=f"<b>Persentase Tingkat Kelulusan - Semua Program Studi ({len(all_prodi_names)} Program Studi)</b>",
        xaxis_title="Program Studi",
        yaxis_title="Persentase (%)",
        barmode='stack',
        height=chart_height,
        title_font_size=16,
        title_x=0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=80, b=200),
        template="plotly_white"
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=8), title_font_size=12)
    fig.update_yaxes(title_font_size=12)
    
    return fig

def create_summary_table(data, all_prodi_names):
    summary_data = []
    for prodi in all_prodi_names:
        prodi_data = data[data['Pilihan 1'] == prodi]
        total_peminat = len(prodi_data)
        lulus = len(prodi_data[prodi_data['Status_Lulus'] == 'Lulus'])
        tidak_lulus = len(prodi_data[prodi_data['Status_Lulus'] == 'Tidak Lulus'])
        tingkat_lulus = (lulus / total_peminat * 100) if total_peminat > 0 else 0
        
        if total_peminat > data['Pilihan 1'].value_counts().quantile(0.8):
            popularity_status = 'Sangat Populer'
        elif total_peminat > data['Pilihan 1'].value_counts().quantile(0.5):
            popularity_status = 'Populer'
        else:
            popularity_status = 'Berkembang'
        
        summary_data.append({
            'Ranking': len(summary_data) + 1,
            'Program Studi': prodi,
            'Total Peminat': total_peminat,
            'Lulus': lulus,
            'Tidak Lulus': tidak_lulus,
            'Tingkat Kelulusan (%)': f"{tingkat_lulus:.1f}%",
            'Status': popularity_status
        })
    
    return pd.DataFrame(summary_data)

def main():
    st.title("Dashboard Analisis Program Studi Universitas")
    st.markdown("")
    st.markdown("---")
    
    df = load_data()
    
    if df is not None:
        st.sidebar.header("Filter Dashboard")
        reset_filter = st.sidebar.button("Reset Filter", use_container_width=True)
        
        jk_options = ['Semua', 'Laki-laki', 'Perempuan']
        selected_jk = st.sidebar.selectbox("Pilih Jenis Kelamin:", jk_options)
        
        # Mapping untuk menampilkan "Bidikmisi" instead of "Bidik Misi"
        bidikmisi_raw = sorted(df['bidikmisi'].unique().tolist())
        bidikmisi_display = []
        bidikmisi_mapping = {}
        
        for item in bidikmisi_raw:
            if item == "Bidik Misi":
                display_name = "Bidikmisi"
                bidikmisi_display.append(display_name)
                bidikmisi_mapping[display_name] = item
            else:
                bidikmisi_display.append(item)
                bidikmisi_mapping[item] = item
        
        bidikmisi_options = ['Semua'] + bidikmisi_display
        selected_bidikmisi_display = st.sidebar.selectbox("Jenis Pendanaan:", bidikmisi_options)
        
        # Convert back to original value for filtering
        if selected_bidikmisi_display == 'Semua':
            selected_bidikmisi = 'Semua'
        else:
            selected_bidikmisi = bidikmisi_mapping.get(selected_bidikmisi_display, selected_bidikmisi_display)
        
        if reset_filter:
            selected_jk = 'Semua'
            selected_bidikmisi = 'Semua'
        
        filtered_df = apply_filters(df, selected_jk, selected_bidikmisi)
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("Statistik Data")
        st.sidebar.metric("Data Terfilter", f"{len(filtered_df):,} mahasiswa")
        st.sidebar.metric("Total Data", f"{len(df):,} mahasiswa")
        filter_percentage = (len(filtered_df) / len(df)) * 100
        st.sidebar.progress(filter_percentage / 100)
        st.sidebar.caption(f"Menampilkan {filter_percentage:.1f}% dari total data")
        
        if not filtered_df.empty:
            col1, col2, col3 = st.columns(3)
            
            total_mahasiswa = len(filtered_df)
            total_prodi = filtered_df['Pilihan 1'].nunique()
            lulus_count = len(filtered_df[filtered_df['Status_Lulus'] == 'Lulus'])
            tingkat_kelulusan = (lulus_count / total_mahasiswa * 100) if total_mahasiswa > 0 else 0
            
            with col1:
                st.markdown("<div style='text-align: center;'><h3>Total Mahasiswa</h3><h2>{:,}</h2></div>".format(total_mahasiswa), unsafe_allow_html=True)
            with col2:
                st.markdown("<div style='text-align: center;'><h3>Program Studi</h3><h2>{}</h2></div>".format(total_prodi), unsafe_allow_html=True)
            with col3:
                st.markdown("<div style='text-align: center;'><h3>Tingkat Kelulusan</h3><h2>{:.1f}%</h2></div>".format(tingkat_kelulusan), unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("Visualisasi Data Program Studi")
            
            col_left, col_right = st.columns([1.2, 1])
            
            with col_left:
                st.markdown("<h4 style='text-align: center;'>Program Studi Terpopuler</h4>", unsafe_allow_html=True)
                fig1, all_prodi = create_popularity_chart(filtered_df)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_right:
                st.markdown("<h4 style='text-align: center;'>Tingkat Kelulusan per Program Studi</h4>", unsafe_allow_html=True)
                fig2 = create_graduation_chart(filtered_df, all_prodi.index.tolist())
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Tabel Ringkasan Program Studi")
            
            summary_df = create_summary_table(filtered_df, all_prodi.index.tolist())
            
            col_search, col_spacer = st.columns([2, 2])
            with col_search:
                search_term = st.text_input("Cari Program Studi:", placeholder="Ketik nama program studi...")
            
            if search_term:
                filtered_summary = summary_df[summary_df['Program Studi'].str.contains(search_term, case=False, na=False)]
            else:
                filtered_summary = summary_df
            
            st.dataframe(
                filtered_summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ranking": st.column_config.NumberColumn("Rank", width="extra_small"),
                    "Program Studi": st.column_config.TextColumn("Program Studi", width="large"),
                    "Total Peminat": st.column_config.NumberColumn("Peminat", width="small"),
                    "Lulus": st.column_config.NumberColumn("Lulus", width="small"),
                    "Tidak Lulus": st.column_config.NumberColumn("Tidak Lulus", width="small"),
                    "Tingkat Kelulusan (%)": st.column_config.TextColumn("Kelulusan", width="small"),
                    "Status": st.column_config.TextColumn("Status", width="medium")
                }
            )
            
            col_empty, col_download = st.columns([3, 1])
            with col_download:
                csv = filtered_summary.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"summary_program_studi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
            st.info("Coba ubah pengaturan filter di sidebar.")
    else:
        st.error("Dashboard tidak dapat dijalankan tanpa data.")

if __name__ == "__main__":
    main()