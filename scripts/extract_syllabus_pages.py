import os
from pypdf import PdfReader, PdfWriter

# Source and destination paths
source_pdf = "Project PDFs/R22B.Tech.CSE(DATASCIENCE)CourseStructureSyllabus2.pdf"
output_pdf = "data/raw/syllabus/cse_ds_scoped_syllabus.pdf"

# Human-readable page numbers (1-indexed, as printed in PDF footer)
human_pages = [46, 47, 54, 58, 59, 66, 69, 74]

# Check if source file exists
if not os.path.exists(source_pdf):
    print(f"Error: Source file not found at {source_pdf}")
    exit(1)

# Create output directory if it doesn't exist
output_dir = os.path.dirname(output_pdf)
os.makedirs(output_dir, exist_ok=True)

# Read the source PDF
reader = PdfReader(source_pdf)

# Create a PDF writer
writer = PdfWriter()

# Convert 1-indexed human page numbers to 0-indexed pypdf page access
# pypdf uses 0-based indexing, so page 46 in the PDF is index 45 in pypdf
pypdf_indices = [page - 1 for page in human_pages]

print(f"Extracting pages (human-readable): {human_pages}")

# Extract the specified pages
for idx in pypdf_indices:
    writer.add_page(reader.pages[idx])

# Write the output PDF
with open(output_pdf, "wb") as output_file:
    writer.write(output_file)

print(f"Output written to: {output_pdf}")

# Verify the output by reopening and counting pages
verification_reader = PdfReader(output_pdf)
page_count = len(verification_reader.pages)

print(f"Verification: Output PDF contains {page_count} pages")
print(f"Expected: {len(human_pages)} pages")

if page_count == len(human_pages):
    print("Page count matches expected")
else:
    print("Page count mismatch!")
