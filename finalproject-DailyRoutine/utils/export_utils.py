"""
Export utilities for DailyRoutine application
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from config.constants import EXPORT_DIR, AUTHOR, NIM, APP_NAME
from database.database import db_manager

class ExportManager:
    """Manager for exporting habit data"""

    def __init__(self, export_dir: str = EXPORT_DIR):
        self.export_dir = export_dir
        self._ensure_export_directory()

    def _ensure_export_directory(self) -> None:
        """Ensure export directory exists"""
        Path(self.export_dir).mkdir(parents=True, exist_ok=True)

    def export_to_csv(self, habits: List[Dict[str, Any]], filename: str = None) -> str:
        """Export habits to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"habits_{timestamp}.csv"

        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                # Define fieldnames
                fieldnames = [
                    'ID', 'Nama', 'Kategori', 'Tanggal Mulai', 'Frekuensi',
                    'Status', 'Prioritas', 'Catatan', 'Streak', 'Total Completed',
                    'Created At', 'Updated At'
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for habit in habits:
                    writer.writerow({
                        'ID': habit.get('id', ''),
                        'Nama': habit.get('name', ''),
                        'Kategori': habit.get('category', ''),
                        'Tanggal Mulai': habit.get('start_date', ''),
                        'Frekuensi': habit.get('frequency', ''),
                        'Status': habit.get('status', ''),
                        'Prioritas': habit.get('priority', ''),
                        'Catatan': habit.get('notes', ''),
                        'Streak': habit.get('streak_count', 0),
                        'Total Completed': habit.get('total_completed', 0),
                        'Created At': habit.get('created_at', ''),
                        'Updated At': habit.get('updated_at', '')
                    })

            return filepath

        except Exception as e:
            raise Exception(f"Error exporting to CSV: {e}")

    def export_to_pdf(self, habits: List[Dict[str, Any]], filename: str = None) -> str:
        """Export habits to PDF file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"habits_report_{timestamp}.pdf"

        filepath = os.path.join(self.export_dir, filename)

        try:
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=inch, bottomMargin=inch)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['h1'],
                fontName='Helvetica-Bold',
                fontSize=22,
                spaceAfter=12,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#212529'),
                leading=28
            )
            title = Paragraph(f"{APP_NAME} - Habit Report", title_style)
            story.append(title)

            # Report info
            info_style = ParagraphStyle(
                'Info',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                spaceAfter=24,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#6c757d'),
                leading=14
            )

            current_time = datetime.now().strftime("%d %B %Y, %H:%M")
            info_text = f"""
            Generated on: {current_time}<br/>
            By: {AUTHOR} (NIM: {NIM})<br/>
            Total Habits in Report: {len(habits)}
            """
            info = Paragraph(info_text, info_style)
            story.append(info)

            # Statistics section
            if habits:
                stats = self._calculate_statistics(habits)
                stats_style = ParagraphStyle(
                    'Stats',
                    parent=styles['Normal'],
                    fontName='Helvetica',
                    fontSize=11,
                    spaceAfter=24,
                    textColor=colors.HexColor('#495057'),
                    leading=18
                )

                stats_text = f"""
                <strong>Summary Statistics:</strong><br/>
                &bull; Total Habits: {stats['total']}<br/>
                &bull; Completed: {stats['completed']} ({stats['completion_rate']:.1f}%)<br/>
                &bull; Pending: {stats['pending']}<br/>
                &bull; High Priority: {stats['high_priority']}<br/>
                &bull; Medium Priority: {stats['medium_priority']}<br/>
                &bull; Low Priority: {stats['low_priority']}
                """
                stats_para = Paragraph(stats_text, stats_style)
                story.append(stats_para)

            # Habits table
            if habits:
                table_data = self._prepare_table_data(habits)
                table = Table(table_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 0.7*inch, 0.8*inch, 0.8*inch])

                # Table styling
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#495057')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white]),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e9ecef')),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('TOPPADDING', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ]))

                story.append(table)

            # Build PDF
            doc.build(story)
            return filepath

        except Exception as e:
            raise Exception(f"Error exporting to PDF: {e}")

    def _calculate_statistics(self, habits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics from habits data"""
        total = len(habits)
        completed = sum(1 for habit in habits if habit.get('status') == 'Selesai')
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0

        high_priority = sum(1 for habit in habits if habit.get('priority') == 'High')
        medium_priority = sum(1 for habit in habits if habit.get('priority') == 'Medium')
        low_priority = sum(1 for habit in habits if habit.get('priority') == 'Low')

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': completion_rate,
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority
        }

    def _prepare_table_data(self, habits: List[Dict[str, Any]]) -> List[List[str]]:
        """Prepare data for PDF table"""
        # Header
        headers = ['ID', 'Nama', 'Kategori', 'Tanggal Mulai', 'Freq', 'Status', 'Prioritas']
        table_data = [headers]

        # Data rows
        for habit in habits:
            row = [
                str(habit.get('id', '')),
                habit.get('name', '')[:20] + '...' if len(habit.get('name', '')) > 20 else habit.get('name', ''),
                habit.get('category', ''),
                habit.get('start_date', '')[:10],  # Just the date part
                str(habit.get('frequency', '')),
                habit.get('status', ''),
                habit.get('priority', '')
            ]
            table_data.append(row)

        return table_data

    def export_all_habits(self, format_type: str = 'pdf') -> str:
        """Export all habits in specified format"""
        try:
            habits = db_manager.get_all_habits()

            if format_type.lower() == 'csv':
                return self.export_to_csv(habits)
            elif format_type.lower() == 'pdf':
                return self.export_to_pdf(habits)
            else:
                raise ValueError(f"Unsupported format: {format_type}")

        except Exception as e:
            raise Exception(f"Error exporting all habits: {e}")

    def export_filtered_habits(self, filters: Dict[str, Any], format_type: str = 'pdf') -> str:
        """Export filtered habits in specified format"""
        try:
            habits = db_manager.get_all_habits(filters)

            if format_type.lower() == 'csv':
                return self.export_to_csv(habits)
            elif format_type.lower() == 'pdf':
                return self.export_to_pdf(habits)
            else:
                raise ValueError(f"Unsupported format: {format_type}")

        except Exception as e:
            raise Exception(f"Error exporting filtered habits: {e}")

# Global export manager instance
export_manager = ExportManager()
