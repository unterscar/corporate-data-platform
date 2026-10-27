# ETL-конвейер Corporate Data Platform
## Инструмент
Для оркестрации обработки данных используется Apache Airflow.

## DAG
corporate_etl

## Источник данных
PostgreSQL, таблица companies.

## Этап Extract
Из PostgreSQL извлекаются поля:
```
id
name
industry
city
employees
```

## Этап Transform
Данные группируются по городам. Для каждого города рассчитываются:
- количество организаций;
- общее количество сотрудников;
- среднее количество сотрудников.

## Этап Load
Результат сохраняется:
```
airflow/output/companies_by_city.csv
```

## Последовательность
extract_companies → transform_companies → load_report

## Расписание
DAG выполняется ежедневно.
