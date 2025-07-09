import json
import os

# List nama file notebook yang mau diekstrak
notebooks = [
    r'shopee-analytics\eda\eda_users.ipynb',
    r'shopee-analytics\eda\eda_orders.ipynb',
    r'shopee-analytics\eda\eda_products.ipynb',
    r'shopee-analytics\eda\eda_payments.ipynb',
    r'shopee-analytics\eda\eda_order_items.ipynb',
]

for nb_path in notebooks:
    # Ambil nama file tanpa ekstensi
    base_name = os.path.splitext(os.path.basename(nb_path))[0]
    output_py = f'{base_name}_code_only.py'

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    code_cells = [cell['source'] for cell in nb['cells'] if cell['cell_type'] == 'code']

    with open(output_py, 'w', encoding='utf-8') as f:
        for i, cell in enumerate(code_cells):
            f.writelines(cell)
            f.write(f'\n\n# --- End of code cell {i+1}\n\n')

    print(f'Extracted {len(code_cells)} code cells from {nb_path} to {output_py}')
