# Exemplos de Import/Export

## Como usar:

### Importar Alunos:
```bash
curl -X POST -F "file=@alunos_exemplo.csv" http://localhost:5000/alunos/import
```

### Importar Professores:
```bash
curl -X POST -F "file=@professores_exemplo.csv" http://localhost:5000/professores/import
```

### Exportar Alunos (CSV):
```bash
curl http://localhost:5000/alunos/export?formato=csv -o alunos_export.csv
```

### Exportar Alunos (JSON):
```bash
curl http://localhost:5000/alunos/export?formato=json -o alunos_export.json
```

### Exportar Pagamentos por período:
```bash
curl "http://localhost:5000/pagamentos/export?mes=06&ano=2023&formato=csv" -o pagamentos_junho.csv
```

## Formatos suportados:
- **Importação**: CSV
- **Exportação**: CSV, JSON