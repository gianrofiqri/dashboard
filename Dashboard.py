import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Analisis Pendaftaran Mahasiswa Universitas Bandung 2023",
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
        df['bidikmisi'] = df['bidikmisi'].astype(str).str.strip()
        df['Pilihan 1'] = df['Pilihan 1'].astype(str).str.strip()
        df['Sekolah'] = df['Sekolah'].astype(str).str.strip()
        return df
    except:
        st.error("File 'Data mahasiswa.csv' tidak ditemukan!")
        return None

def apply_filters(df, bidikmisi_filter, provinsi_filter):
    filtered_df = df.copy()
    if bidikmisi_filter != 'Semua':
        filtered_df = filtered_df[filtered_df['bidikmisi'] == bidikmisi_filter]
    if provinsi_filter != 'Semua':
        filtered_df = filtered_df[filtered_df['Provinsi'] == provinsi_filter]
    return filtered_df

def create_popularity_chart(data):
    all_prodi = data['Pilihan 1'].value_counts()
    
    fig = px.pie(
        values=all_prodi.values,
        names=all_prodi.index,
        title=f"<b>Distribusi Pendaftar per Program Studi ({len(all_prodi)} Program Studi)</b>",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=9,
        pull=0,
        hovertemplate='<b>Program Studi:</b> %{label}<br><b>Jumlah Pendaftar:</b> %{value}<br><b>Persentase:</b> %{percent}<extra></extra>'
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

def create_acceptance_chart(data, all_prodi_names):
    df_all_prodi = data[data['Pilihan 1'].isin(all_prodi_names)]
    prodi_lulus_crosstab = pd.crosstab(df_all_prodi['Pilihan 1'], df_all_prodi['Status_Lulus'], normalize='index') * 100
    prodi_lulus_crosstab = prodi_lulus_crosstab.reindex(all_prodi_names)
    
    acceptance_rates = []
    prodi_names = []
    
    for prodi in all_prodi_names:
        prodi_data = data[data['Pilihan 1'] == prodi]
        total_pendaftar = len(prodi_data)
        diterima = len(prodi_data[prodi_data['Status_Lulus'] == 'Lulus'])
        acceptance_rate = (diterima / total_pendaftar * 100) if total_pendaftar > 0 else 0
        
        acceptance_rates.append(acceptance_rate)
        prodi_names.append(prodi)
    
    fig = go.Figure()
    chart_height = max(600, min(1200, len(all_prodi_names) * 30))
    
    fig.add_trace(go.Bar(
        name='Tingkat Penerimaan',
        x=prodi_names,
        y=acceptance_rates,
        marker_color='#2E8B57',  
        text=[f'{val:.1f}' for val in acceptance_rates],
        textposition='outside',
        textfont=dict(color='black', size=10),
        hovertemplate='<b>Program Studi:</b> %{x}<br><b>Tingkat Penerimaan:</b> %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"<b>Tingkat Penerimaan per Program Studi - Universitas Bandung 2023</b>",
        xaxis_title="Program Studi",
        yaxis_title="Tingkat Penerimaan (%)",
        height=chart_height,
        title_font_size=16,
        title_x=0.5,
        margin=dict(l=50, r=50, t=80, b=200),
        template="plotly_white"
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=8), title_font_size=12)
    fig.update_yaxes(title_font_size=12, range=[0, 100])
    
    return fig

def create_competition_analysis(data):
    """Analisis tingkat persaingan untuk membantu calon mahasiswa"""
    prodi_stats = []
    
    for prodi in data['Pilihan 1'].unique():
        prodi_data = data[data['Pilihan 1'] == prodi]
        total_pendaftar = len(prodi_data)
        diterima = len(prodi_data[prodi_data['Status_Lulus'] == 'Lulus'])
        tingkat_penerimaan = (diterima / total_pendaftar * 100) if total_pendaftar > 0 else 0
        
        if tingkat_penerimaan >= 70:
            kategori_persaingan = "Mudah"
            warna = "#28a745"  
        elif tingkat_penerimaan >= 40:
            kategori_persaingan = "Sedang"
            warna = "#ffc107"  
        else:
            kategori_persaingan = "Sulit"
            warna = "#dc3545"  
        
        prodi_stats.append({
            'Program Studi': prodi,
            'Total Pendaftar': total_pendaftar,
            'Diterima': diterima,
            'Tingkat Penerimaan': tingkat_penerimaan,
            'Kategori Persaingan': kategori_persaingan,
            'Warna': warna
        })
    
    return pd.DataFrame(prodi_stats).sort_values('Total Pendaftar', ascending=False)

def create_summary_table(data, all_prodi_names):
    summary_data = []
    for i, prodi in enumerate(all_prodi_names):
        prodi_data = data[data['Pilihan 1'] == prodi]
        total_pendaftar = len(prodi_data)
        diterima = len(prodi_data[prodi_data['Status_Lulus'] == 'Lulus'])
        tidak_diterima = total_pendaftar - diterima
        tingkat_penerimaan = (diterima / total_pendaftar * 100) if total_pendaftar > 0 else 0
        
        if tingkat_penerimaan >= 70:
            kategori = "Peluang Tinggi"
        elif tingkat_penerimaan >= 40:
            kategori = "Peluang Sedang"
        else:
            kategori = "Peluang Rendah"
     
        bidikmisi_count = len(prodi_data[prodi_data['bidikmisi'] == 'Bidik Misi'])
        
        summary_data.append({
            'Ranking': i + 1,
            'Program Studi': prodi,
            'Total Pendaftar': total_pendaftar,
            'Diterima': diterima,
            'Tidak Diterima': tidak_diterima,
            'Tingkat Penerimaan': f"{tingkat_penerimaan:.1f}%",
            'Pendaftar Bidikmisi': bidikmisi_count,
            'Kategori Peluang': kategori
        })
    
    return pd.DataFrame(summary_data)

def main():
    st.title("Dashboard Analisis Pendaftaran Mahasiswa Universitas Bandung Tahun Penerimaan 2023")
    st.markdown("---")
    
    df = load_data()
    
    if df is not None:
        st.sidebar.header("Filter Dashboard")
        reset_filter = st.sidebar.button("Reset Filter", use_container_width=True)
       
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
 
        provinsi_options = ['Semua'] + sorted(df['Provinsi'].dropna().unique().tolist())
        selected_provinsi = st.sidebar.selectbox("Asal Provinsi:", provinsi_options)
      
        if selected_bidikmisi_display == 'Semua':
            selected_bidikmisi = 'Semua'
        else:
            selected_bidikmisi = bidikmisi_mapping.get(selected_bidikmisi_display, selected_bidikmisi_display)
        
        if reset_filter:
            selected_bidikmisi = 'Semua'
            selected_provinsi = 'Semua'
        
        filtered_df = apply_filters(df, selected_bidikmisi, selected_provinsi)
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("Statistik Data Terpilih")
        st.sidebar.metric("Data Terfilter", f"{len(filtered_df):,} pendaftar")
        st.sidebar.metric("Total Data", f"{len(df):,} pendaftar")
        filter_percentage = (len(filtered_df) / len(df)) * 100
        st.sidebar.progress(filter_percentage / 100)
        st.sidebar.caption(f"Menampilkan {filter_percentage:.1f}% dari total data")
        
        if not filtered_df.empty:

            col1, col2, col3, col4 = st.columns(4)
            
            total_pendaftar = len(filtered_df)
            total_prodi = filtered_df['Pilihan 1'].nunique()
            total_diterima = len(filtered_df[filtered_df['Status_Lulus'] == 'Lulus'])
            tingkat_penerimaan_keseluruhan = (total_diterima / total_pendaftar * 100) if total_pendaftar > 0 else 0
            
            with col1:
                st.markdown("<div style='text-align: center; background-color: #e3f2fd; padding: 20px; border-radius: 10px;'><h3 style='color: #1976d2;'>Total Pendaftar</h3><h2 style='color: #1976d2;'>{:,}</h2></div>".format(total_pendaftar), unsafe_allow_html=True)
            with col2:
                st.markdown("<div style='text-align: center; background-color: #e8f5e8; padding: 20px; border-radius: 10px;'><h3 style='color: #2e7d32;'>Diterima</h3><h2 style='color: #2e7d32;'>{:,}</h2></div>".format(total_diterima), unsafe_allow_html=True)
            with col3:
                st.markdown("<div style='text-align: center; background-color: #fff3e0; padding: 20px; border-radius: 10px;'><h3 style='color: #f57c00;'>Program Studi</h3><h2 style='color: #f57c00;'>{}</h2></div>".format(total_prodi), unsafe_allow_html=True)
            with col4:
                st.markdown("<div style='text-align: center; background-color: #fce4ec; padding: 20px; border-radius: 10px;'><h3 style='color: #c2185b;'>Tingkat Penerimaan</h3><h2 style='color: #c2185b;'>{:.1f}%</h2></div>".format(tingkat_penerimaan_keseluruhan), unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("Visualisasi Data Pendaftaran")
            
            col_left, col_right = st.columns([1.2, 1])
            
            with col_left:
                st.markdown("<h4 style='text-align: center;'>Distribusi Pendaftar per Program Studi</h4>", unsafe_allow_html=True)
                fig1, all_prodi = create_popularity_chart(filtered_df)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_right:
                st.markdown("<h4 style='text-align: center;'>Tingkat Penerimaan per Program Studi</h4>", unsafe_allow_html=True)
                fig2 = create_acceptance_chart(filtered_df, all_prodi.index.tolist())
                st.plotly_chart(fig2, use_container_width=True)
            
            
            st.markdown("---")
            st.subheader("Tabel Ringkasan Lengkap - Data Pendaftaran per Program Studi")
            
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
                    "Total Pendaftar": st.column_config.NumberColumn("Total Pendaftar", width="small"),
                    "Diterima": st.column_config.NumberColumn("Diterima", width="small"),
                    "Tidak Diterima": st.column_config.NumberColumn("Tidak Diterima", width="small"),
                    "Tingkat Penerimaan": st.column_config.TextColumn("Tingkat Penerimaan", width="small"),
                    "Pendaftar Bidikmisi": st.column_config.NumberColumn("Bidikmisi", width="small"),
                    "Kategori Peluang": st.column_config.TextColumn("Kategori Peluang", width="medium")
                }
            )
            
            
            col_empty, col_download = st.columns([3, 1])
            with col_download:
                csv = filtered_summary.to_csv(index=False)
                st.download_button(
                    label="Download Data CSV",
                    data=csv,
                    file_name=f"data_pendaftaran_univ_bandung_2023_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
            st.info("Coba ubah pengaturan filter di sidebar untuk melihat data.")
    else:
        st.error("Dashboard tidak dapat dijalankan tanpa data.")

if __name__ == "__main__":
    main()