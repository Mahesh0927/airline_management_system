from fpdf import FPDF

def generate_boarding_pass_pdf(t):
    # Initialize PDF in Landscape (Boarding Pass dimensions)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- BRAND COLORS ---
    navy = (0, 31, 46)
    gold = (255, 193, 7)
    
    # --- TICKET BORDER ---
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(10, 10, 277, 85) # Outer Frame

    # --- HEADER BLOCK (NAVY) ---
    pdf.set_fill_color(*navy)
    pdf.rect(10, 10, 277, 20, 'F')
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.set_xy(15, 15)
    pdf.cell(100, 10, "BOUNDLESS AIR", 0, 0, 'L')
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(210, 15)
    pdf.cell(70, 10, "BOARDING PASS / E-TICKET", 0, 0, 'R')

    # --- PERFORATION LINE (Stub Divider) ---
    pdf.set_draw_color(150, 150, 150)
    pdf.dashed_line(210, 10, 210, 95, 1, 1)

    # --- LEFT SIDE: MAIN TICKET CONTENT ---
    pdf.set_text_color(0, 0, 0)
    
    # 1. Passenger Name
    pdf.set_font("Arial", '', 9)
    pdf.set_xy(15, 35)
    pdf.cell(40, 5, "PASSENGER NAME", 0, 1)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_x(15)
    pdf.cell(100, 8, str(t['passenger_name']).upper(), 0, 1)

    # 2. Origin and Destination (Large Codes)
    pdf.set_font("Arial", 'B', 35)
    pdf.set_xy(15, 55)
    pdf.cell(40, 15, t['src_code'], 0, 0)
    pdf.set_font("Arial", '', 15)
    pdf.cell(20, 15, ">>>", 0, 0, 'C')
    pdf.set_font("Arial", 'B', 35)
    pdf.cell(40, 15, t['dst_code'], 0, 1)
    
    pdf.set_font("Arial", '', 8)
    pdf.set_xy(15, 75)
    pdf.cell(40, 5, str(t['src']).upper(), 0, 0)
    pdf.set_x(75)
    pdf.cell(40, 5, str(t['dst']).upper(), 0, 1)

    # 3. Flight Details Grid
    pdf.set_font("Arial", '', 9)
    pdf.set_xy(120, 35)
    pdf.cell(30, 5, "FLIGHT", 0, 0)
    pdf.cell(30, 5, "DATE", 0, 0)
    pdf.cell(30, 5, "CLASS", 0, 1)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_x(120)
    pdf.cell(30, 8, t['flight_num'], 0, 0)
    pdf.cell(30, 8, t['dep_time'].strftime('%d %b %y'), 0, 0)
    pdf.cell(30, 8, str(t['class']).upper(), 0, 1)

    pdf.ln(2)
    pdf.set_font("Arial", '', 9)
    pdf.set_x(120)
    pdf.cell(30, 5, "BOARDING", 0, 0)
    pdf.cell(30, 5, "SEAT", 0, 0)
    pdf.cell(30, 5, "GATE", 0, 1)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_x(120)
    pdf.cell(30, 8, t['dep_time'].strftime('%H:%M'), 0, 0)
    pdf.set_text_color(*navy)
    pdf.cell(30, 8, t['seat_num'], 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(30, 8, "G-12", 0, 1)

    # --- RIGHT SIDE: STUB (FOR AIRLINE) ---
    pdf.set_xy(215, 35)
    pdf.set_font("Arial", '', 8)
    pdf.cell(60, 5, "PASSENGER", 0, 1)
    pdf.set_x(215)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(60, 5, str(t['passenger_name']).upper(), 0, 1)
    
    pdf.ln(5)
    pdf.set_x(215)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(25, 10, t['src_code'], 0, 0)
    pdf.cell(25, 10, t['dst_code'], 0, 1)

    pdf.set_font("Arial", '', 8)
    pdf.set_x(215)
    pdf.cell(20, 5, "FLIGHT", 0, 0)
    pdf.cell(20, 5, "SEAT", 0, 0)
    pdf.cell(20, 5, "DATE", 0, 1)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.set_x(215)
    pdf.cell(20, 5, t['flight_num'], 0, 0)
    pdf.cell(20, 5, t['seat_num'], 0, 0)
    pdf.cell(20, 5, t['dep_time'].strftime('%d %b'), 0, 1)

    # --- BARCODE SIMULATION ---
    pdf.set_fill_color(0,0,0)
    pdf.rect(15, 82, 100, 8, 'F') 
    pdf.set_fill_color(255, 255, 255)
    for i in range(15, 115, 3):
        pdf.rect(i, 82, 1, 8, 'F')
        
    pdf.set_fill_color(0,0,0)
    pdf.rect(215, 82, 55, 8, 'F')
    pdf.set_fill_color(255, 255, 255)
    for i in range(215, 270, 4):
        pdf.rect(i, 82, 1.5, 8, 'F')

    # --- GOLD ACCENT LINE ---
    pdf.set_fill_color(*gold)
    pdf.rect(10, 95, 277, 2, 'F')

    # --- FOOTER ---
    pdf.set_xy(10, 100)
    pdf.set_text_color(150, 150, 150)
    pdf.set_font("Arial", 'I', 7)
    pdf.multi_cell(277, 4, "THIS IS AN ELECTRONIC TICKET. PLEASE PRESENT VALID ID AT THE AIRPORT. BOARDING GATE CLOSES 25 MINS PRIOR TO DEPARTURE.", 0, 'C')

    return pdf.output()