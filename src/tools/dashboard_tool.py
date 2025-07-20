# from crewai.tools import BaseTool
# from typing import Type, Optional, Dict, Any, List
# from pydantic import BaseModel, Field
# import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.utils import PlotlyJSONEncoder
# import json
# import os
# from datetime import datetime


# class DashboardInput(BaseModel):
#     """Input schema for Dashboard Tool."""
#     data_source: str = Field(..., description="Path to data file or data as JSON string")
#     chart_type: str = Field(..., description="Type of chart: 'line', 'bar', 'pie', 'scatter', 'histogram'")
#     x_column: Optional[str] = Field(None, description="Column name for x-axis")
#     y_column: Optional[str] = Field(None, description="Column name for y-axis")
#     title: Optional[str] = Field("Dashboard Chart", description="Chart title")
#     color_column: Optional[str] = Field(None, description="Column for color grouping")
#     output_path: Optional[str] = Field("results/Dashboard/Dashboard_Agent_inventory.html", description="Output HTML file path")

# class DashboardTool(BaseTool):
#     name: str = "Dashboard Builder"
#     description: str = (
#         "Creates interactive dashboards with charts from data. "
#         "Supports various chart types: line, bar, pie, scatter, histogram. "
#         "Can read CSV files or JSON data and generate HTML dashboard."
#     )
#     args_schema: Type[BaseModel] = DashboardInput

#     def _run(self, data_source: str, chart_type: str, x_column: str = None, 
#              y_column: str = None, title: str = "Dashboard Chart", 
#              color_column: str = None, output_path: str = "results/Dashboard/Dashboard_Agent_inventory.html") -> str:
#         try:
#             # Load data
#             df = self._load_data(data_source)
            
#             # Create chart based on type
#             fig = self._create_chart(df, chart_type, x_column, y_column, title, color_column)
            
#             # Generate HTML dashboard
#             html_content = self._generate_html_dashboard(fig, title)
            
#             # Save dashboard
#             with open(output_path, 'w', encoding='utf-8') as f:
#                 f.write(html_content)
            
#             return f"Dashboard created successfully at: {output_path}"
            
#         except Exception as e:
#             return f"Error creating dashboard: {str(e)}"

#     def _load_data(self, data_source: str) -> pd.DataFrame:
#         """Load data from file or JSON string."""
#         if data_source.endswith('.csv'):
#             return pd.read_csv(data_source)
#         elif data_source.endswith('.xlsx') or data_source.endswith('.xls'):
#             return pd.read_excel(data_source)
#         else:
#             # Try to parse as JSON
#             try:
#                 data = json.loads(data_source)
#                 return pd.DataFrame(data)
#             except:
#                 raise ValueError("Unsupported data format")

#     def _create_chart(self, df: pd.DataFrame, chart_type: str, x_column: str, 
#                      y_column: str, title: str, color_column: str = None) -> go.Figure:
#         """Create chart based on specified type."""
        
#         if chart_type == 'line':
#             fig = px.line(df, x=x_column, y=y_column, color=color_column, title=title)
#         elif chart_type == 'bar':
#             fig = px.bar(df, x=x_column, y=y_column, color=color_column, title=title)
#         elif chart_type == 'pie':
#             fig = px.pie(df, values=y_column, names=x_column, title=title)
#         elif chart_type == 'scatter':
#             fig = px.scatter(df, x=x_column, y=y_column, color=color_column, title=title)
#         elif chart_type == 'histogram':
#             fig = px.histogram(df, x=x_column, color=color_column, title=title)
#         else:
#             # Default to bar chart
#             fig = px.bar(df, x=x_column, y=y_column, title=title)
        
#         # Update layout for better appearance
#         fig.update_layout(
#             template='plotly_white',
#             font=dict(family="Arial", size=12),
#             title_font_size=16,
#             showlegend=True
#         )
        
#         return fig

#     def _generate_html_dashboard(self, fig: go.Figure, title: str) -> str:
#         """Generate complete HTML dashboard."""
        
#         # Convert figure to JSON
#         fig_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        
#         html_template = f"""
# <!DOCTYPE html>
# <html>
# <head>
#     <title>{title}</title>
#     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             margin: 0;
#             padding: 20px;
#             background-color: #f5f5f5;
#         }}
#         .container {{
#             max-width: 1200px;
#             margin: 0 auto;
#             background-color: white;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#         }}
#         .header {{
#             text-align: center;
#             margin-bottom: 30px;
#             color: #333;
#         }}
#         .chart-container {{
#             width: 100%;
#             height: 600px;
#             margin-bottom: 20px;
#         }}
#         .info {{
#             background-color: #f8f9fa;
#             padding: 15px;
#             border-radius: 5px;
#             margin-top: 20px;
#         }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>{title}</h1>
#             <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
#         </div>
        
#         <div class="chart-container" id="chart"></div>
        
#         <div class="info">
#             <h3>Dashboard Information</h3>
#             <p>This dashboard was automatically generated using CrewAI Dashboard Tool</p>
#             <p>Interactive features: Zoom, Pan, Hover for details</p>
#         </div>
#     </div>

#     <script>
#         var figure = {fig_json};
#         Plotly.newPlot('chart', figure.data, figure.layout, {{responsive: true}});
#     </script>
# </body>
# </html>
# """
#         return html_template

from crewai.tools import BaseTool
from typing import Type, Optional, Dict, Any, List
from pydantic import BaseModel, Field
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import os
from datetime import datetime
import numpy as np
from plotly.subplots import make_subplots
import ast


class DashboardInput(BaseModel):
    """Input schema for Comprehensive Dashboard Tool."""
    data_source: str = Field(..., description="Path to data file or data as JSON string")
    title: Optional[str] = Field("Complete Data Analysis Dashboard", description="Dashboard title")
    output_path: Optional[str] = Field("results/Dashboard/Complete_Dashboard.html", description="Output HTML file path")
    
class ComprehensiveDashboardTool(BaseTool):
    name: str = "Comprehensive Dashboard Builder"
    description: str = (
        "Creates a complete interactive dashboard with comprehensive data analysis. "
        "Shows statistics, multiple charts, data tables, insights, and trends. "
        "Provides full overview of your data with professional visualizations."
    )
    args_schema: Type[BaseModel] = DashboardInput

    def _run(self, data_source: str, title: str = "Complete Data Analysis Dashboard", 
             output_path: str = "results/Dashboard/Complete_Dashboard.html") -> str:
        try:
            # Load data
            df = self._load_data(data_source)
            
            # Analyze data comprehensively
            analysis = self._comprehensive_analysis(df)
            
            # Create all charts
            charts = self._create_all_charts(df, analysis)
            
            # Generate complete HTML dashboard
            html_content = self._generate_complete_dashboard(df, analysis, charts, title)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save dashboard
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return f"Complete dashboard created successfully at: {output_path}"
            
        except Exception as e:
            return f"Error creating dashboard: {str(e)}"

    def _load_data(self, data_source: str) -> pd.DataFrame:
        """Load data from file or JSON string."""
    
        if os.path.exists(data_source):
            if data_source.endswith('.csv'):
                return pd.read_csv(data_source)
            elif data_source.endswith('.xlsx') or data_source.endswith('.xls'):
                return pd.read_excel(data_source)
            else:
                raise ValueError("Unsupported file type.")
        else:
            try:
                data = json.loads(data_source)
                return pd.DataFrame(data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string or file path not found.")


    def _comprehensive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive data analysis."""
        
        analysis = {
            'basic_info': {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'column_names': list(df.columns),
                'data_types': df.dtypes.to_dict(),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'missing_values': df.isnull().sum().to_dict()
            },
            'numerical_stats': {},
            'categorical_stats': {},
            'insights': [],
            'correlations': {},
            'top_values': {}
        }
        
        # Numerical columns analysis
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            analysis['numerical_stats'] = df[numerical_cols].describe().to_dict()
            
            # Correlations for numerical columns
            if len(numerical_cols) > 1:
                analysis['correlations'] = df[numerical_cols].corr().to_dict()
        
        # Categorical columns analysis
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            analysis['categorical_stats'][col] = {
                'unique_values': df[col].nunique(),
                'top_values': df[col].value_counts().head(10).to_dict(),
                'missing_count': df[col].isnull().sum()
            }
        
        # Generate insights
        analysis['insights'] = self._generate_insights(df, analysis)
        
        # Top values for key columns
        for col in df.columns:
            if df[col].dtype == 'object':
                analysis['top_values'][col] = df[col].value_counts().head(5).to_dict()
        
        return analysis

    def _generate_insights(self, df: pd.DataFrame, analysis: Dict) -> List[str]:
        """Generate data insights."""
        insights = []
        
        # Basic insights
        insights.append(f"Dataset contains {analysis['basic_info']['total_rows']:,} rows and {analysis['basic_info']['total_columns']} columns")
        
        # Missing values insights
        missing_cols = [col for col, count in analysis['basic_info']['missing_values'].items() if count > 0]
        if missing_cols:
            insights.append(f"Missing values found in {len(missing_cols)} columns: {', '.join(missing_cols[:3])}")
        
        # Numerical insights
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            insights.append(f"Dataset has {len(numerical_cols)} numerical columns for quantitative analysis")
            
            # Find highest correlation
            if len(numerical_cols) > 1:
                corr_matrix = df[numerical_cols].corr()
                # Get highest correlation (excluding diagonal)
                mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
                corr_matrix = corr_matrix.mask(mask)
                max_corr = corr_matrix.abs().max().max()
                if not pd.isna(max_corr):
                    insights.append(f"Highest correlation coefficient: {max_corr:.3f}")
        
        # Categorical insights
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            insights.append(f"Dataset has {len(categorical_cols)} categorical columns")
        
        return insights

    def _create_all_charts(self, df: pd.DataFrame, analysis: Dict) -> Dict[str, str]:
        """Create all charts for the dashboard."""
        charts = {}
        
        # 1. Data Overview Chart
        charts['overview'] = self._create_overview_chart(df, analysis)
        
        # 2. Numerical distributions
        charts['numerical_dist'] = self._create_numerical_distributions(df)
        
        # 3. Categorical distributions
        charts['categorical_dist'] = self._create_categorical_distributions(df)
        
        # 4. Correlation heatmap
        charts['correlation'] = self._create_correlation_heatmap(df)
        
        # 5. Missing values chart
        charts['missing_values'] = self._create_missing_values_chart(df)
        
        # 6. Time series (if date columns exist)
        charts['time_series'] = self._create_time_series_chart(df)
        
        # 7. Summary statistics
        charts['summary_stats'] = self._create_summary_stats_chart(df)
        
        return charts

    def _create_overview_chart(self, df: pd.DataFrame, analysis: Dict) -> str:
        """Create data overview chart."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Data Types', 'Missing Values', 'Column Count', 'Row Count'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Data types pie chart
        dtype_counts = pd.Series(analysis['basic_info']['data_types']).value_counts()
        fig.add_trace(go.Pie(labels=dtype_counts.index, values=dtype_counts.values, name="Data Types"), row=1, col=1)
        
        # Missing values bar chart
        missing_data = pd.Series(analysis['basic_info']['missing_values'])
        missing_data = missing_data[missing_data > 0]
        if len(missing_data) > 0:
            fig.add_trace(go.Bar(x=missing_data.index, y=missing_data.values, name="Missing Values"), row=1, col=2)
        
        # Column count indicator
        fig.add_trace(go.Indicator(
            mode="number",
            value=analysis['basic_info']['total_columns'],
            title={"text": "Total Columns"}
        ), row=2, col=1)
        
        # Row count indicator
        fig.add_trace(go.Indicator(
            mode="number",
            value=analysis['basic_info']['total_rows'],
            title={"text": "Total Rows"}
        ), row=2, col=2)
        
        fig.update_layout(height=600, showlegend=False, title_text="Data Overview")
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def _create_numerical_distributions(self, df: pd.DataFrame) -> str:
        """Create numerical distributions chart."""
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) == 0:
            return json.dumps(go.Figure().add_annotation(text="No numerical columns found", 
                                                       xref="paper", yref="paper", x=0.5, y=0.5, 
                                                       showarrow=False), cls=PlotlyJSONEncoder)
        
        # Create subplots for histograms
        cols = min(3, len(numerical_cols))
        rows = (len(numerical_cols) + cols - 1) // cols
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=numerical_cols.tolist()
        )
        
        for i, col in enumerate(numerical_cols):
            row = i // cols + 1
            col_pos = i % cols + 1
            
            fig.add_trace(
                go.Histogram(x=df[col], name=col, showlegend=False),
                row=row, col=col_pos
            )
        
        fig.update_layout(height=200 * rows, title_text="Numerical Distributions")
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def _create_categorical_distributions(self, df: pd.DataFrame) -> str:
        """Create categorical distributions chart."""
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) == 0:
            return json.dumps(go.Figure().add_annotation(text="No categorical columns found", 
                                                       xref="paper", yref="paper", x=0.5, y=0.5, 
                                                       showarrow=False), cls=PlotlyJSONEncoder)
        
        # Create subplots for bar charts
        cols = min(2, len(categorical_cols))
        rows = (len(categorical_cols) + cols - 1) // cols
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=categorical_cols.tolist()
        )
        
        for i, col in enumerate(categorical_cols):
            row = i // cols + 1
            col_pos = i % cols + 1
            
            value_counts = df[col].value_counts().head(10)
            
            fig.add_trace(
                go.Bar(x=value_counts.index, y=value_counts.values, name=col, showlegend=False),
                row=row, col=col_pos
            )
        
        fig.update_layout(height=300 * rows, title_text="Categorical Distributions")
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def _create_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """Create correlation heatmap."""
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) < 2:
            return json.dumps(go.Figure().add_annotation(text="Need at least 2 numerical columns for correlation", 
                                                       xref="paper", yref="paper", x=0.5, y=0.5, 
                                                       showarrow=False), cls=PlotlyJSONEncoder)
        
        corr_matrix = df[numerical_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(3).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Correlation Matrix",
            xaxis_title="Features",
            yaxis_title="Features",
            height=500
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def _create_missing_values_chart(self, df: pd.DataFrame) -> str:
        """Create missing values visualization."""
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0]
        
        if len(missing_data) == 0:
            return json.dumps(go.Figure().add_annotation(text="No missing values found! 🎉", 
                                                       xref="paper", yref="paper", x=0.5, y=0.5, 
                                                       showarrow=False), cls=PlotlyJSONEncoder)
        
        fig = go.Figure(data=[
            go.Bar(x=missing_data.index, y=missing_data.values, 
                   text=missing_data.values, textposition='auto')
        ])
        
        fig.update_layout(
            title="Missing Values by Column",
            xaxis_title="Columns",
            yaxis_title="Missing Count",
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def _create_time_series_chart(self, df: pd.DataFrame) -> str:
        """Create time series chart if date columns exist."""
        # Try to find date columns
        date_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col].head(100), errors='raise')
                    date_cols.append(col)
                except:
                    continue
        
        if len(date_cols) == 0:
            return json.dumps(go.Figure().add_annotation(text="No date columns detected", 
                                                       xref="paper", yref="paper", x=0.5, y=0.5, 
                                                       showarrow=False), cls=PlotlyJSONEncoder)
        
        # Use first date column
        date_col = date_cols[0]
        df_copy = df.copy()
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
        
        # Count records by date
        date_counts = df_copy[date_col].value_counts().sort_index()
        
        fig = go.Figure(data=go.Scatter(
            x=date_counts.index,
            y=date_counts.values,
            mode='lines+markers',
            name='Records Count'
        ))
        
        fig.update_layout(
            title=f"Time Series: Records by {date_col}",
            xaxis_title=date_col,
            yaxis_title="Count",
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def _create_summary_stats_chart(self, df: pd.DataFrame) -> str:
        """Create summary statistics chart."""
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) == 0:
            return json.dumps(go.Figure().add_annotation(text="No numerical columns for statistics", 
                                                       xref="paper", yref="paper", x=0.5, y=0.5, 
                                                       showarrow=False), cls=PlotlyJSONEncoder)
        
        stats = df[numerical_cols].describe()
        
        fig = go.Figure(data=go.Heatmap(
            z=stats.values,
            x=stats.columns,
            y=stats.index,
            colorscale='Viridis',
            text=stats.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Summary Statistics",
            xaxis_title="Columns",
            yaxis_title="Statistics",
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)


    def _generate_complete_dashboard(self, df: pd.DataFrame, analysis: Dict, charts: Dict, title: str) -> str:
        
        """Generate complete HTML dashboard."""

        # Create data table HTML
        table_html = df.head(100).to_html(classes='table table-striped table-hover', table_id='data-table')

        # Create insights HTML
        insights_html = ''.join([f'<li class="insight-item">{insight}</li>' for insight in analysis['insights']])

        # Create statistics HTML
        stats_html = ""
        if analysis['numerical_stats']:
            stats_df = pd.DataFrame(analysis['numerical_stats'])
            stats_html = stats_df.to_html(classes='table table-bordered')

        # Create statistics section HTML safely
        stats_section_html = ""
        if stats_html:
            stats_section_html = f"""
            <div class="section">
                <h2><i class="fas fa-table"></i> Summary Statistics</h2>
                <div class="table-container">
                    {stats_html}
                </div>
            </div>
            """

        html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }}
            .dashboard-container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .dashboard-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .dashboard-header h1 {{
                margin: 0;
                font-size: 2.5rem;
                font-weight: 300;
            }}
            .dashboard-header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            .dashboard-content {{
                padding: 30px;
            }}
            .section {{
                margin-bottom: 40px;
                border-radius: 10px;
                background: #f8f9fa;
                padding: 25px;
            }}
            .section h2 {{
                color: #495057;
                margin-bottom: 20px;
                font-size: 1.8rem;
                font-weight: 500;
            }}
            .chart-container {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            .stat-card {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-card h3 {{
                color: #667eea;
                margin-bottom: 10px;
            }}
            .stat-card .stat-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #495057;
            }}
            .insights-list {{
                list-style: none;
                padding: 0;
            }}
            .insight-item {{
                background: white;
                margin-bottom: 10px;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .table-container {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                overflow-x: auto;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .table {{
                font-size: 0.9rem;
            }}
            .nav-tabs {{
                margin-bottom: 20px;
            }}
            .nav-link {{
                color: #667eea;
            }}
            .nav-link.active {{
                background-color: #667eea;
                border-color: #667eea;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-top: 1px solid #dee2e6;
            }}
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="dashboard-header">
                <h1><i class="fas fa-chart-line"></i> {title}</h1>
                <p><i class="fas fa-calendar"></i> Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            </div>
            
            <div class="dashboard-content">
                <!-- Key Statistics -->
                <div class="section">
                    <h2><i class="fas fa-tachometer-alt"></i> Key Statistics</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3><i class="fas fa-table"></i> Total Records</h3>
                            <div class="stat-value">{analysis['basic_info']['total_rows']:,}</div>
                        </div>
                        <div class="stat-card">
                            <h3><i class="fas fa-columns"></i> Total Columns</h3>
                            <div class="stat-value">{analysis['basic_info']['total_columns']}</div>
                        </div>
                        <div class="stat-card">
                            <h3><i class="fas fa-database"></i> Memory Usage</h3>
                            <div class="stat-value">{analysis['basic_info']['memory_usage'] / 1024:.1f} KB</div>
                        </div>
                        <div class="stat-card">
                            <h3><i class="fas fa-exclamation-triangle"></i> Missing Values</h3>
                            <div class="stat-value">{sum(analysis['basic_info']['missing_values'].values())}</div>
                        </div>
                    </div>
                </div>
                
                <!-- Data Insights -->
                <div class="section">
                    <h2><i class="fas fa-lightbulb"></i> Data Insights</h2>
                    <ul class="insights-list">
                        {insights_html}
                    </ul>
                </div>
                
                <!-- Visualizations -->
                <div class="section">
                    <h2><i class="fas fa-chart-bar"></i> Data Visualizations</h2>
                    <ul class="nav nav-tabs" id="chartTabs" role="tablist">
                        <li class="nav-item"><button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button" role="tab"><i class="fas fa-eye"></i> Overview</button></li>
                        <li class="nav-item"><button class="nav-link" id="numerical-tab" data-bs-toggle="tab" data-bs-target="#numerical" type="button" role="tab"><i class="fas fa-calculator"></i> Numerical</button></li>
                        <li class="nav-item"><button class="nav-link" id="categorical-tab" data-bs-toggle="tab" data-bs-target="#categorical" type="button" role="tab"><i class="fas fa-tags"></i> Categorical</button></li>
                        <li class="nav-item"><button class="nav-link" id="correlation-tab" data-bs-toggle="tab" data-bs-target="#correlation" type="button" role="tab"><i class="fas fa-project-diagram"></i> Correlation</button></li>
                        <li class="nav-item"><button class="nav-link" id="missing-tab" data-bs-toggle="tab" data-bs-target="#missing" type="button" role="tab"><i class="fas fa-question-circle"></i> Missing Values</button></li>
                        <li class="nav-item"><button class="nav-link" id="time-tab" data-bs-toggle="tab" data-bs-target="#time" type="button" role="tab"><i class="fas fa-clock"></i> Time Series</button></li>
                        <li class="nav-item"><button class="nav-link" id="stats-tab" data-bs-toggle="tab" data-bs-target="#stats" type="button" role="tab"><i class="fas fa-chart-area"></i> Statistics</button></li>
                    </ul>

                    <div class="tab-content" id="chartTabsContent">
                        <div class="tab-pane fade show active" id="overview"><div class="chart-container" id="overview-chart"></div></div>
                        <div class="tab-pane fade" id="numerical"><div class="chart-container" id="numerical-chart"></div></div>
                        <div class="tab-pane fade" id="categorical"><div class="chart-container" id="categorical-chart"></div></div>
                        <div class="tab-pane fade" id="correlation"><div class="chart-container" id="correlation-chart"></div></div>
                        <div class="tab-pane fade" id="missing"><div class="chart-container" id="missing-chart"></div></div>
                        <div class="tab-pane fade" id="time"><div class="chart-container" id="time-chart"></div></div>
                        <div class="tab-pane fade" id="stats"><div class="chart-container" id="stats-chart"></div></div>
                    </div>
                </div>

                <!-- Summary Statistics Table -->
                {stats_section_html}

                <!-- Data Sample -->
                <div class="section">
                    <h2><i class="fas fa-database"></i> Data Sample (First 100 rows)</h2>
                    <div class="table-container">
                        {table_html}
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p><i class="fas fa-robot"></i> Generated by CrewAI Comprehensive Dashboard Tool</p>
                <p>Interactive Dashboard with Complete Data Analysis</p>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            const charts = {{
                overview: {charts['overview']},
                numerical: {charts['numerical_dist']},
                categorical: {charts['categorical_dist']},
                correlation: {charts['correlation']},
                missing: {charts['missing_values']},
                time: {charts['time_series']},
                stats: {charts['summary_stats']}
            }};
            function initializeCharts() {{
                Object.keys(charts).forEach(chartType => {{
                    const containerId = chartType + '-chart';
                    const container = document.getElementById(containerId);
                    if (container) {{
                        Plotly.newPlot(containerId, charts[chartType].data, charts[chartType].layout, {{
                            responsive: true,
                            displayModeBar: true,
                            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
                        }});
                    }}
                }});
            }}
            document.addEventListener('DOMContentLoaded', function() {{
                initializeCharts();
                const tabTriggerList = [].slice.call(document.querySelectorAll('#chartTabs button'));
                tabTriggerList.forEach(function (tabTrigger) {{
                    tabTrigger.addEventListener('shown.bs.tab', function () {{
                        setTimeout(initializeCharts, 100);
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """
        return html_template
