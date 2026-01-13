results=./UI_allure_results
rep_history=./UI_final-report/history
report=./UI_final-report

rm -rf $results # Удалить папку с результатами
pytest test_UI.py --alluredir=UI_allure_results # Запустить тесты 
mv $rep_history $results # Перенести историю в результаты 
rm -rf $report # Удалить отчет
allure generate $results -o $report # Сгенерировать отчет
allure open $report # Открыть отчет