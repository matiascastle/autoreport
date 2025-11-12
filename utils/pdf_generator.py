"""
Módulo para generar PDFs profesionales de reportes.
Estructura: 4 páginas (Executive Summary, Performance, Trends, Action Items)
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import os
from typing import Dict, Any, List


class PDFReportGenerator:
    """Genera reportes PDF profesionales de 4 páginas."""
    
    def __init__(self, client_name: str, data: Dict[str, Any], output_path: str = "report.pdf"):
        self.client_name = client_name
        self.data = data
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal mejorado
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            leading=14
        ))
        
        # Insight destacado
        self.styles.add(ParagraphStyle(
            name='Insight',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#27ae60'),
            spaceAfter=10,
            leftIndent=20,
            fontName='Helvetica-Bold'
        ))
    
    def generate(self) -> str:
        """Genera el PDF completo."""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Página 1: Executive Summary
        story.extend(self._create_page_1())
        story.append(PageBreak())
        
        # Página 2: Performance Deep Dive
        story.extend(self._create_page_2())
        story.append(PageBreak())
        
        # Página 3: Trends & Insights
        story.extend(self._create_page_3())
        story.append(PageBreak())
        
        # Página 4: Action Items
        story.extend(self._create_page_4())
        
        # Build PDF
        doc.build(story)
        
        return self.output_path
    
    def _create_page_1(self) -> List:
        """Página 1: Executive Summary."""
        elements = []
        
        # Header
        elements.append(Paragraph(
            f"📊 {self.client_name} Weekly Report",
            self.styles['CustomTitle']
        ))
        
        # Fecha
        current_date = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(
            f"Generated: {current_date}",
            self.styles['CustomBody']
        ))
        
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1f77b4')))
        elements.append(Spacer(1, 20))
        
        # Key Metrics Table
        elements.append(Paragraph("KEY METRICS", self.styles['CustomSubtitle']))
        
        metrics = self.data.get('metrics', {})
        metrics_data = [['Metric', 'Value', 'Change']]
        
        for key, metric in metrics.items():
            value = metric['value']
            label = metric['label']
            format_type = metric.get('format', 'number')
            
            if format_type == 'currency':
                value_str = f"${value:,.2f}"
            elif format_type == 'percentage':
                value_str = f"{value:.1f}%"
            else:
                value_str = f"{value:,.0f}"
            
            # Simular cambio (en producción, calcular real)
            change = "↑ 12%" if 'growth' not in key else f"{value:+.1f}%"
            
            metrics_data.append([label, value_str, change])
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 1.5*inch, 1*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 30))
        
        # Quick Insights
        elements.append(Paragraph("QUICK INSIGHTS", self.styles['CustomSubtitle']))
        
        insights = self.data.get('insights', [])
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", self.styles['Insight']))
        
        elements.append(Spacer(1, 20))
        
        # Summary text
        elements.append(Paragraph(
            "<b>Summary:</b> Overall performance shows positive trends across key metrics. "
            "Revenue growth is strong, and customer engagement remains high. "
            "Continue monitoring top-performing categories for optimization opportunities.",
            self.styles['CustomBody']
        ))
        
        return elements
    
    def _create_page_2(self) -> List:
        """Página 2: Performance Deep Dive."""
        elements = []
        
        elements.append(Paragraph("PERFORMANCE DEEP DIVE", self.styles['CustomTitle']))
        elements.append(Spacer(1, 20))
        
        # Revenue Breakdown
        elements.append(Paragraph("Revenue Breakdown", self.styles['CustomSubtitle']))
        
        charts = self.data.get('charts', {})
        
        # Crear gráfico de línea simple (Revenue Over Time)
        if charts.get('line_chart'):
            line_data = charts['line_chart']
            
            # Descripción del gráfico
            elements.append(Paragraph(
                f"<b>{line_data['title']}</b>",
                self.styles['CustomBody']
            ))
            
            # Tabla con datos de tendencia
            trend_data = [['Date', 'Revenue']]
            x_data = line_data['x_data'][-7:]  # Últimos 7 días
            y_data = line_data['y_data'][-7:]
            
            for date, revenue in zip(x_data, y_data):
                trend_data.append([str(date)[:10], f"${revenue:,.2f}"])
            
            trend_table = Table(trend_data, colWidths=[2.5*inch, 2.5*inch])
            trend_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.95, 0.95, 0.95)),
            ]))
            
            elements.append(trend_table)
            elements.append(Spacer(1, 20))
        
        # Category Performance
        if charts.get('pie_chart'):
            pie_data = charts['pie_chart']
            
            elements.append(Paragraph("Category Performance", self.styles['CustomSubtitle']))
            
            category_data = [['Category', 'Revenue', '% of Total']]
            total = sum(pie_data['values'])
            
            for label, value in zip(pie_data['labels'][:5], pie_data['values'][:5]):
                percentage = (value / total * 100) if total > 0 else 0
                category_data.append([
                    str(label),
                    f"${value:,.2f}",
                    f"{percentage:.1f}%"
                ])
            
            category_table = Table(category_data, colWidths=[2*inch, 1.75*inch, 1.25*inch])
            category_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.95, 0.98, 0.95)),
            ]))
            
            elements.append(category_table)
        
        elements.append(Spacer(1, 20))
        
        # Performance Analysis
        elements.append(Paragraph("Analysis", self.styles['CustomSubtitle']))
        elements.append(Paragraph(
            "Key performance indicators show consistent growth across all major categories. "
            "The data reveals strong customer demand and effective marketing strategies. "
            "Top-performing segments continue to drive the majority of revenue.",
            self.styles['CustomBody']
        ))
        
        return elements
    
    def _create_page_3(self) -> List:
        """Página 3: Trends & Insights."""
        elements = []
        
        elements.append(Paragraph("TRENDS & INSIGHTS", self.styles['CustomTitle']))
        elements.append(Spacer(1, 20))
        
        # Key Trends
        elements.append(Paragraph("Key Trends Identified", self.styles['CustomSubtitle']))
        
        trends = [
            ("Revenue Growth", "↑ 12%", "Strong upward trend in overall revenue compared to previous period"),
            ("Customer Engagement", "↑ 8%", "Increased customer interaction and repeat purchases"),
            ("Top Categories", "Stable", "Consistent performance from best-selling product lines"),
            ("New Opportunities", "+3", "Emerging categories showing potential for growth")
        ]
        
        trends_data = [['Trend', 'Change', 'Description']]
        for trend, change, desc in trends:
            trends_data.append([trend, change, desc])
        
        trends_table = Table(trends_data, colWidths=[1.5*inch, 0.75*inch, 3*inch])
        trends_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.98, 0.95, 0.95)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(trends_table)
        elements.append(Spacer(1, 30))
        
        # Insights Deep Dive
        elements.append(Paragraph("Detailed Insights", self.styles['CustomSubtitle']))
        
        insights_text = [
            "<b>Customer Behavior:</b> Analysis shows increased purchasing frequency, "
            "particularly in high-value categories. Customer retention rates remain strong.",
            
            "<b>Product Performance:</b> Top-performing products continue to drive revenue growth. "
            "Consider expanding inventory in these categories to meet demand.",
            
            "<b>Market Opportunities:</b> Emerging trends indicate potential for new product lines. "
            "Early adoption could provide competitive advantage.",
            
            "<b>Operational Efficiency:</b> Current processes support growth trajectory. "
            "Minor optimizations could further improve margins."
        ]
        
        for insight in insights_text:
            elements.append(Paragraph(insight, self.styles['CustomBody']))
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _create_page_4(self) -> List:
        """Página 4: Action Items & Recommendations."""
        elements = []
        
        elements.append(Paragraph("ACTION ITEMS & RECOMMENDATIONS", self.styles['CustomTitle']))
        elements.append(Spacer(1, 20))
        
        # Priority Actions
        elements.append(Paragraph("Priority Actions", self.styles['CustomSubtitle']))
        
        actions_data = [
            ['Priority', 'Action', 'Timeline', 'Impact'],
            ['HIGH', 'Expand top-performing category inventory', '1-2 weeks', 'High'],
            ['HIGH', 'Launch targeted marketing for emerging products', '2-3 weeks', 'Medium'],
            ['MEDIUM', 'Optimize pricing strategy for mid-tier products', '3-4 weeks', 'Medium'],
            ['MEDIUM', 'Improve customer retention programs', '4-6 weeks', 'High'],
            ['LOW', 'Review and update product descriptions', '6-8 weeks', 'Low']
        ]
        
        actions_table = Table(actions_data, colWidths=[0.8*inch, 2.5*inch, 1*inch, 0.7*inch])
        actions_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.97, 0.95, 0.98)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(actions_table)
        elements.append(Spacer(1, 30))
        
        # Recommendations
        elements.append(Paragraph("Strategic Recommendations", self.styles['CustomSubtitle']))
        
        recommendations = [
            ("<b>Short-term (1-3 months):</b>", 
             "Focus on maximizing revenue from existing top performers while testing new product introductions. "
             "Monitor customer feedback closely and adjust inventory levels accordingly."),
            
            ("<b>Medium-term (3-6 months):</b>", 
             "Expand into emerging categories showing strong early indicators. "
             "Develop comprehensive marketing campaigns to support new product launches."),
            
            ("<b>Long-term (6-12 months):</b>", 
             "Build brand loyalty through enhanced customer experience initiatives. "
             "Consider strategic partnerships to expand market reach and product offerings.")
        ]
        
        for title, text in recommendations:
            elements.append(Paragraph(title, self.styles['CustomBody']))
            elements.append(Paragraph(text, self.styles['CustomBody']))
            elements.append(Spacer(1, 10))
        
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1, 10))
        
        # Footer
        elements.append(Paragraph(
            f"<i>This report was automatically generated for {self.client_name} on {datetime.now().strftime('%B %d, %Y')}. "
            "For questions or additional analysis, please contact your account manager.</i>",
            self.styles['CustomBody']
        ))
        
        return elements

