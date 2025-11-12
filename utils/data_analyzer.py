"""
Módulo para análisis automático de datos de cualquier empresa.
Detecta tipos de columnas y genera métricas inteligentes.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class DataAnalyzer:
    """Analiza CSVs automáticamente y detecta tipos de datos."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.detected_columns = self._detect_columns()
    
    def _detect_columns(self) -> Dict[str, Any]:
        """Detecta automáticamente tipo de dato y genera métricas."""
        results = {
            'numeric': [],
            'dates': [],
            'categories': [],
            'metrics': {},
            'column_info': {}
        }
        
        for col in self.df.columns:
            col_lower = col.lower()
            
            # Detecta fechas
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                results['dates'].append(col)
                results['column_info'][col] = 'date'
            elif any(date_keyword in col_lower for date_keyword in ['date', 'time', 'day', 'month', 'year', 'fecha']):
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    results['dates'].append(col)
                    results['column_info'][col] = 'date'
                except:
                    pass
            
            # Detecta numéricos
            if pd.api.types.is_numeric_dtype(self.df[col]) or self._is_numeric_string(col):
                results['numeric'].append(col)
                
                # ¿Es dinero?
                if any(keyword in col_lower for keyword in ['revenue', 'price', 'cost', 'sales', 'total', 'amount', 'ingreso', 'venta', 'precio']):
                    results['metrics'][col] = 'currency'
                    results['column_info'][col] = 'currency'
                
                # ¿Es porcentaje?
                elif any(keyword in col_lower for keyword in ['rate', 'percent', '%', 'pct', 'ratio', 'tasa', 'porcentaje']):
                    results['metrics'][col] = 'percentage'
                    results['column_info'][col] = 'percentage'
                
                # ¿Es cantidad?
                elif any(keyword in col_lower for keyword in ['quantity', 'count', 'orders', 'units', 'cantidad', 'pedidos']):
                    results['metrics'][col] = 'count'
                    results['column_info'][col] = 'count'
                
                # Default: número
                else:
                    results['metrics'][col] = 'number'
                    results['column_info'][col] = 'number'
            
            # Detecta categorías
            elif pd.api.types.is_string_dtype(self.df[col]) or pd.api.types.is_object_dtype(self.df[col]):
                if col not in results['dates']:  # No es fecha
                    results['categories'].append(col)
                    results['column_info'][col] = 'category'
        
        return results
    
    def _is_numeric_string(self, col: str) -> bool:
        """Detecta si una columna de strings contiene números."""
        try:
            sample = self.df[col].dropna().head(10)
            if len(sample) == 0:
                return False
            
            # Intenta convertir a numérico
            pd.to_numeric(sample.astype(str).str.replace(',', '').str.replace('$', '').str.replace('%', ''))
            return True
        except:
            return False
    
    def get_key_metrics(self) -> Dict[str, Any]:
        """Genera métricas clave automáticamente."""
        metrics = {}
        
        # Encuentra columnas principales
        revenue_cols = [col for col in self.detected_columns['numeric'] 
                       if self.detected_columns['metrics'].get(col) == 'currency']
        count_cols = [col for col in self.detected_columns['numeric'] 
                     if self.detected_columns['metrics'].get(col) == 'count']
        date_cols = self.detected_columns['dates']
        
        # Revenue total
        if revenue_cols:
            main_revenue = revenue_cols[0]
            metrics['total_revenue'] = {
                'value': float(self.df[main_revenue].sum()),
                'label': 'Total Revenue',
                'format': 'currency'
            }
            
            # AOV (Average Order Value)
            if count_cols:
                order_col = count_cols[0]
                total_orders = self.df[order_col].sum()
                if total_orders > 0:
                    metrics['aov'] = {
                        'value': float(self.df[main_revenue].sum() / total_orders),
                        'label': 'Average Order Value',
                        'format': 'currency'
                    }
        
        # Total de órdenes/cantidad
        if count_cols:
            main_count = count_cols[0]
            metrics['total_orders'] = {
                'value': int(self.df[main_count].sum()),
                'label': f'Total {main_count.title()}',
                'format': 'number'
            }
        
        # Total de registros
        metrics['total_records'] = {
            'value': len(self.df),
            'label': 'Total Records',
            'format': 'number'
        }
        
        # Clientes únicos (si hay columna de cliente)
        customer_cols = [col for col in self.detected_columns['categories'] 
                        if any(keyword in col.lower() for keyword in ['customer', 'client', 'user', 'cliente', 'usuario'])]
        if customer_cols:
            metrics['unique_customers'] = {
                'value': int(self.df[customer_cols[0]].nunique()),
                'label': 'Unique Customers',
                'format': 'number'
            }
        
        # Growth (si hay fechas)
        if date_cols and revenue_cols:
            date_col = date_cols[0]
            revenue_col = revenue_cols[0]
            
            try:
                df_sorted = self.df.sort_values(date_col)
                df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
                
                # Últimos 7 días vs 7 días anteriores
                latest_date = df_sorted[date_col].max()
                week_ago = latest_date - pd.Timedelta(days=7)
                two_weeks_ago = latest_date - pd.Timedelta(days=14)
                
                current_week = df_sorted[df_sorted[date_col] >= week_ago][revenue_col].sum()
                previous_week = df_sorted[(df_sorted[date_col] >= two_weeks_ago) & (df_sorted[date_col] < week_ago)][revenue_col].sum()
                
                if previous_week > 0:
                    growth = ((current_week - previous_week) / previous_week) * 100
                    metrics['growth'] = {
                        'value': float(growth),
                        'label': 'Growth vs Last Week',
                        'format': 'percentage'
                    }
            except:
                pass
        
        return metrics
    
    def get_chart_data(self) -> Dict[str, Any]:
        """Genera datos para charts automáticamente."""
        charts = {
            'line_chart': None,
            'pie_chart': None,
            'bar_chart': None
        }
        
        date_cols = self.detected_columns['dates']
        revenue_cols = [col for col in self.detected_columns['numeric'] 
                       if self.detected_columns['metrics'].get(col) == 'currency']
        category_cols = self.detected_columns['categories']
        
        # Line Chart: Fecha + Revenue
        if date_cols and revenue_cols:
            date_col = date_cols[0]
            revenue_col = revenue_cols[0]
            
            try:
                df_grouped = self.df.groupby(date_col)[revenue_col].sum().reset_index()
                df_grouped = df_grouped.sort_values(date_col)
                
                charts['line_chart'] = {
                    'title': f'{revenue_col} Over Time',
                    'x_data': df_grouped[date_col].astype(str).tolist(),
                    'y_data': df_grouped[revenue_col].tolist(),
                    'x_label': date_col,
                    'y_label': revenue_col
                }
            except Exception as e:
                print(f"Error creating line chart: {e}")
        
        # Pie Chart: Categoría + Revenue
        if category_cols and revenue_cols:
            category_col = category_cols[0]
            revenue_col = revenue_cols[0]
            
            try:
                df_grouped = self.df.groupby(category_col)[revenue_col].sum().reset_index()
                df_grouped = df_grouped.sort_values(revenue_col, ascending=False).head(10)
                
                charts['pie_chart'] = {
                    'title': f'{revenue_col} by {category_col}',
                    'labels': df_grouped[category_col].tolist(),
                    'values': df_grouped[revenue_col].tolist()
                }
            except Exception as e:
                print(f"Error creating pie chart: {e}")
        
        # Bar Chart: Top 10 categorías
        if category_cols and revenue_cols:
            category_col = category_cols[0]
            revenue_col = revenue_cols[0]
            
            try:
                df_grouped = self.df.groupby(category_col)[revenue_col].sum().reset_index()
                df_grouped = df_grouped.sort_values(revenue_col, ascending=False).head(10)
                
                charts['bar_chart'] = {
                    'title': f'Top 10 {category_col}',
                    'x_data': df_grouped[category_col].tolist(),
                    'y_data': df_grouped[revenue_col].tolist()
                }
            except Exception as e:
                print(f"Error creating bar chart: {e}")
        
        return charts
    
    def get_insights(self) -> List[str]:
        """Genera insights automáticos."""
        insights = []
        
        metrics = self.get_key_metrics()
        
        # Insight de revenue
        if 'total_revenue' in metrics:
            revenue = metrics['total_revenue']['value']
            insights.append(f"✅ Total revenue: ${revenue:,.2f}")
        
        # Insight de growth
        if 'growth' in metrics:
            growth = metrics['growth']['value']
            emoji = "📈" if growth > 0 else "📉"
            insights.append(f"{emoji} Growth vs last week: {growth:+.1f}%")
        
        # Insight de AOV
        if 'aov' in metrics:
            aov = metrics['aov']['value']
            insights.append(f"💰 Average order value: ${aov:.2f}")
        
        # Insight de top category
        charts = self.get_chart_data()
        if charts['pie_chart']:
            top_category = charts['pie_chart']['labels'][0]
            top_value = charts['pie_chart']['values'][0]
            insights.append(f"🏆 Top category: {top_category} (${top_value:,.2f})")
        
        return insights

