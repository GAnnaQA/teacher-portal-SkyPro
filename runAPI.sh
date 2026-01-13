results=./API_allure_results
rep_history=./API_final-report/history
report=./API_final-report

rm -rf $results # Удалить папку с результатами
pytest test_API.py --alluredir=API_allure_results # Запустить тесты 
mv $rep_history $results # Перенести историю в результаты 
rm -rf $report # Удалить отчет
allure generate $results -o $report # Сгенерировать отчет
allure open $report # Открыть отчет