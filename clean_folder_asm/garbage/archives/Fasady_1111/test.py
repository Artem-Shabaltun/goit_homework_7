def save_applicant_data(source, output):
    with open(output, 'w') as file:
        lines = []
        for applicant in source:
            line = f"{applicant['name']},{applicant['specialty']},{applicant['math']},{applicant['lang']},{applicant['eng']}\n"
            lines.append(line)
        file.writelines(lines)