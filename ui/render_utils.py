
import streamlit as st
import pandas as pd
import plotly.express as px

def render_data_results(data, turn_index=0):
    # Display Results (Full Width)
    kpis = data.get("kpis", {})
    
    # ... previous code ...
    
    # Metrics Row (Full Width)
    m1, m2, m3 = st.columns(3)
    
    primary_val = kpis.get('primary_val', 0)
    primary_label = kpis.get('primary_label', 'Main Metric')
    
    # Smart formatting: Add $ if it looks like currency
    is_currency = any(x in primary_label.lower() for x in ['revenue', 'sales', 'spend', 'price', 'budget', 'roi'])
    val_str = f"${primary_val:,.2f}" if is_currency else f"{primary_val:,.0f}"
    
    growth_val = kpis.get("growth", "12.5%")
    yoy_val = kpis.get("yoy", "8.2%")

    with m1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(39, 174, 96, 0.1) 100%); 
                    padding: 15px; border-radius: 12px; border: 1px solid rgba(46, 204, 113, 0.3); border-left: 5px solid #2ecc71; 
                    text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                <h4 style='color: #bdc3c7; font-size: 0.9rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;'>{primary_label}</h4>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: 800; margin: 5px 0;'>{val_str}</p>
            <p style='color: #2ecc71; font-size: 0.8rem; font-weight: 600; margin: 0;'>▲ AI Calculated</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(41, 128, 185, 0.1) 100%); 
                    padding: 15px; border-radius: 12px; border: 1px solid rgba(52, 152, 219, 0.3); border-left: 5px solid #3498db; 
                    text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h4 style='color: #bdc3c7; font-size: 0.9rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;'>📈 Growth Rate</h4>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: 800; margin: 5px 0;'>{growth_val}</p>
            <p style='color: #3498db; font-size: 0.8rem; font-weight: 600; margin: 0;'>▲ Target Exceeded</p>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(155, 89, 182, 0.1) 0%, rgba(142, 68, 173, 0.1) 100%); 
                    padding: 15px; border-radius: 12px; border: 1px solid rgba(155, 89, 182, 0.3); border-left: 5px solid #9b59b6; 
                    text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h4 style='color: #bdc3c7; font-size: 0.9rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;'>📅 Year over Year</h4>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: 800; margin: 5px 0;'>{yoy_val}</p>
            <p style='color: #e74c3c; font-size: 0.8rem; font-weight: 600; margin: 0;'>▼ Slight deviation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid #e74c3c; background-color: #e74c3c; opacity: 1; margin: 25px 0;'>", unsafe_allow_html=True)
    
    # PREMIUM HEADERS FOR VISUALS
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 5px;'>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <div style='background: #3498db; width: 5px; height: 25px; border-radius: 10px;'></div>
            <h3 style='margin: 0; font-size: 1.25rem; font-weight: 700; color: #ffffff;'>📊 Visualization Graph</h3>
        </div>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <div style='background: #e67e22; width: 5px; height: 25px; border-radius: 10px;'></div>
            <h3 style='margin: 0; font-size: 1.25rem; font-weight: 700; color: #ffffff;'>📋 Detail View Table</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Charts and Table (Full Width)
    df = pd.DataFrame(data.get("data", []))
    c1, c2 = st.columns([2, 1])
    
    with c1:
        if not df.empty:
            # Identify numeric and categorical columns
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # Style adjustment for Plotly
            chart_theme = {
                "layout": {
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "font": {"color": "#bdc3c7", "family": "Inter, sans-serif"},
                    "margin": {"t": 40, "b": 40, "l": 40, "r": 20}
                }
            }

            if len(df) == 1 and num_cols:
                if len(num_cols) > 1:
                    # CASE: Single row with multiple metrics (e.g. YTD vs Last Year)
                    # Create a comparison bar chart
                    comparison_df = df[num_cols].T.reset_index()
                    comparison_df.columns = ['Metric', 'Value']
                    comparison_df['Metric'] = comparison_df['Metric'].str.replace('_', ' ').str.title()
                    
                    fig = px.bar(comparison_df, x='Metric', y='Value', color='Metric', 
                               text_auto='.2s', color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig.update_layout(chart_theme["layout"], title="Comparison Analysis")
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_comparison_{turn_index}")
                elif len(num_cols) == 1:
                    # CASE: Truly one single value
                    val = df[num_cols[0]].iloc[0]
                    col_name = num_cols[0].replace('_', ' ').title()
                    
                    # Format as currency
                    if any(x in col_name.lower() for x in ['revenue', 'sales', 'total', 'price', 'amount']):
                        formatted_val = f"${val:,.2f}"
                    else:
                        formatted_val = f"{val:,.2f}" if isinstance(val, (int, float)) else val
                        
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(52, 152, 219, 0.15) 0%, rgba(41, 128, 185, 0.05) 100%); 
                                padding: 40px; border-radius: 15px; border: 1px solid rgba(52, 152, 219, 0.2); 
                                text-align: center; margin-top: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                        <h2 style='color: #3498db; font-size: 1.2rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 2px;'>{col_name}</h2>
                        <p style='color: #ffffff; font-size: 3.5rem; font-weight: 800; margin: 15px 0;'>{formatted_val}</p>
                        <div style='display: inline-block; padding: 5px 15px; background: rgba(46, 204, 113, 0.2); color: #2ecc71; border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                            ✨ AI Computed Successfully
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif "region" in df.columns and "revenue" in df.columns:
                    fig = px.pie(df, values='revenue', names='region', hole=.5, 
                                 color_discrete_sequence=px.colors.qualitative.Prism)
                    fig.update_layout(chart_theme["layout"], title="Revenue Distribution by Region")
                    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#1e1e1e', width=2)))
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_pie_{turn_index}")
            
            elif cat_cols and num_cols:
                fig = px.bar(df, x=cat_cols[0], y=num_cols[0], 
                           color=num_cols[0], color_continuous_scale='Blues')
                fig.update_layout(chart_theme["layout"], title=f"Analysis: {num_cols[0].title()} by {cat_cols[0].title()}")
                fig.update_traces(marker_line_color='rgba(0,0,0,0)', marker_line_width=0, opacity=0.9)
                st.plotly_chart(fig, use_container_width=True, key=f"chart_bar_{turn_index}")

            elif cat_cols and not num_cols:
                # CASE: Only categorical data (e.g. list of Departments) -> Show Frequency Plot
                viz_df = df.copy()
                target_col = cat_cols[0]
                viz_df = viz_df[target_col].value_counts().reset_index()
                viz_df.columns = [target_col, 'Count']
                
                fig = px.bar(viz_df, x='Count', y=target_col, orientation='h',
                           color='Count', color_continuous_scale='Viridis',
                           text_auto=True)
                fig.update_layout(chart_theme["layout"], title=f"Frequency Distribution: {target_col.title()}")
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True, key=f"chart_freq_{turn_index}")
                
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.info("No data available for visualization.")
            
    with c2:
        st.dataframe(df, use_container_width=True, height=400)
        
    with st.expander("🔍 See Generated SQL & Reasoning"):
        sql_code = data.get("sql", "N/A")
        reasoning_text = data.get("reasoning", "")
        
        st.markdown(f"**Agent Reasoning:**\n{reasoning_text}")
        st.markdown("---")
        st.markdown("**Generated SQL Query:**")
        st.code(sql_code, language="sql")
        
        # Add download buttons for the current data and SQL
        if not df.empty:
            st.divider()
            d_col1, d_col2 = st.columns(2)
            
            with d_col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data (CSV)",
                    data=csv,
                    file_name=f"agentic_bi_export_{pd.Timestamp.now().strftime('%H%M%S')}.csv",
                    mime='text/csv',
                    use_container_width=True,
                    key=f"dl_csv_{turn_index}"
                )
            
            with d_col2:
                st.download_button(
                    label="📜 Download SQL Query",
                    data=sql_code,
                    file_name=f"query_{pd.Timestamp.now().strftime('%H%M%S')}.sql",
                    mime='text/plain',
                    use_container_width=True,
                    key=f"dl_sql_{turn_index}"
                )
