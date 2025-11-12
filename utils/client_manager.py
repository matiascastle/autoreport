"""
Módulo para gestión de clientes y envío de emails.
Incluye almacenamiento simple en JSON y envío de reportes por email.
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, 
                                   FileName, FileType, Disposition)
import base64


class ClientManager:
    """Gestiona clientes y sus reportes."""
    
    def __init__(self, data_file: str = "clients_data.json"):
        self.data_file = data_file
        self.clients = self._load_clients()
    
    def _load_clients(self) -> List[Dict]:
        """Carga clientes desde archivo JSON."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_clients(self):
        """Guarda clientes en archivo JSON."""
        with open(self.data_file, 'w') as f:
            json.dump(self.clients, f, indent=2)
    
    def add_client(self, name: str, email: str, company: str = "", 
                   brand_color: str = "#1f77b4") -> Dict:
        """Añade un nuevo cliente."""
        client = {
            'id': len(self.clients) + 1,
            'name': name,
            'email': email,
            'company': company,
            'brand_color': brand_color,
            'created_at': datetime.now().isoformat(),
            'reports': []
        }
        
        self.clients.append(client)
        self._save_clients()
        
        return client
    
    def get_client(self, client_id: int) -> Optional[Dict]:
        """Obtiene un cliente por ID."""
        for client in self.clients:
            if client['id'] == client_id:
                return client
        return None
    
    def get_client_by_email(self, email: str) -> Optional[Dict]:
        """Obtiene un cliente por email."""
        for client in self.clients:
            if client['email'].lower() == email.lower():
                return client
        return None
    
    def update_client(self, client_id: int, **kwargs):
        """Actualiza información de un cliente."""
        for i, client in enumerate(self.clients):
            if client['id'] == client_id:
                self.clients[i].update(kwargs)
                self._save_clients()
                return self.clients[i]
        return None
    
    def delete_client(self, client_id: int) -> bool:
        """Elimina un cliente."""
        self.clients = [c for c in self.clients if c['id'] != client_id]
        self._save_clients()
        return True
    
    def add_report_to_client(self, client_id: int, report_data: Dict):
        """Añade un reporte al historial del cliente."""
        client = self.get_client(client_id)
        if client:
            report = {
                'date': datetime.now().isoformat(),
                'metrics': report_data.get('metrics', {}),
                'pdf_path': report_data.get('pdf_path', '')
            }
            
            for i, c in enumerate(self.clients):
                if c['id'] == client_id:
                    if 'reports' not in self.clients[i]:
                        self.clients[i]['reports'] = []
                    self.clients[i]['reports'].append(report)
                    break
            
            self._save_clients()
            return report
        return None
    
    def get_client_reports(self, client_id: int) -> List[Dict]:
        """Obtiene historial de reportes de un cliente."""
        client = self.get_client(client_id)
        if client:
            return client.get('reports', [])
        return []
    
    def get_all_clients(self) -> List[Dict]:
        """Obtiene todos los clientes."""
        return self.clients


class EmailSender:
    """Envía emails con reportes adjuntos."""
    
    def __init__(self, api_key: Optional[str] = None, from_email: Optional[str] = None):
        self.api_key = api_key or os.getenv('SENDGRID_API_KEY')
        self.from_email = from_email or os.getenv('SENDGRID_FROM_EMAIL', 'reports@autoreport.io')
        
        if self.api_key:
            self.sg = SendGridAPIClient(self.api_key)
        else:
            self.sg = None
    
    def send_report(self, to_email: str, client_name: str, 
                   pdf_path: str, subject: Optional[str] = None) -> bool:
        """Envía reporte por email con PDF adjunto."""
        
        if not self.sg:
            print("⚠️  SendGrid API key not configured. Email not sent.")
            return False
        
        # Subject
        if not subject:
            subject = f"📊 Your Weekly Report - {datetime.now().strftime('%B %d, %Y')}"
        
        # HTML Content
        html_content = self._create_email_html(client_name)
        
        # Crear mensaje
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        # Adjuntar PDF
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                data = f.read()
            
            encoded_file = base64.b64encode(data).decode()
            
            attached_file = Attachment(
                FileContent(encoded_file),
                FileName(f'report_{datetime.now().strftime("%Y%m%d")}.pdf'),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.attachment = attached_file
        
        try:
            response = self.sg.send(message)
            print(f"✅ Email sent! Status code: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _create_email_html(self, client_name: str) -> str:
        """Crea el contenido HTML del email."""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #1f77b4 0%, #1557b0 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    background: #1f77b4;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 30px;
                }}
                .metrics {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .metric-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Your Weekly Report is Ready!</h1>
                <p>{datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="content">
                <p>Hi {client_name},</p>
                
                <p>Your weekly performance report is now available. We've analyzed your data and generated comprehensive insights to help you make informed decisions.</p>
                
                <div class="metrics">
                    <h3 style="margin-top: 0;">📈 Quick Overview</h3>
                    <p>Your detailed 4-page report includes:</p>
                    <ul>
                        <li><strong>Executive Summary</strong> - Key metrics at a glance</li>
                        <li><strong>Performance Analysis</strong> - Deep dive into your data</li>
                        <li><strong>Trends & Insights</strong> - What's working and why</li>
                        <li><strong>Action Items</strong> - Recommendations for growth</li>
                    </ul>
                </div>
                
                <p>The full report is attached as a PDF. Review it at your convenience and feel free to reach out if you have any questions.</p>
                
                <p style="margin-top: 30px;">
                    <strong>Best regards,</strong><br>
                    AutoReport Team
                </p>
            </div>
            
            <div class="footer">
                <p>This is an automated report generated by AutoReport.</p>
                <p>© {datetime.now().year} AutoReport. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_test_email(self, to_email: str) -> bool:
        """Envía un email de prueba."""
        
        if not self.sg:
            print("⚠️  SendGrid API key not configured.")
            return False
        
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject='Test Email from AutoReport',
            html_content='<p>This is a test email. Your SendGrid configuration is working correctly! ✅</p>'
        )
        
        try:
            response = self.sg.send(message)
            print(f"✅ Test email sent! Status code: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Error sending test email: {e}")
            return False

