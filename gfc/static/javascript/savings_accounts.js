function roundToDecimalPlaces(element, dp) {
    element.value = parseFloat(element.value).toFixed(dp);
    if (dp == 0) {
      element.value = parseInt(element.value);
    }
  }

function getUserChoices() {
    // Retrieves the user selection for the account and the projection timescale (in months)
    accountIDs = JSON.parse(document.getElementById('accountDropdown').value);
    const accountsInfo = JSON.parse("{{bank_account_infos|escapejs}}");
    const conversionsDict = JSON.parse("{{conversion_to_main_currency_JSON|escapejs}}");
    const projectionTimescaleInMonths = document.getElementById('projectionTimescaleDropdown').value;
    const currencyChosen = document.getElementById('currencyDropdown').value;

    selectedCurrency= "{{main_currency}}";

    if (currencyChosen != "DEFAULT") {
        selectedCurrency = currencyChosen;
    }
    else if (accountIDs.length == 1) {
        selectedCurrency = accountsInfo[accountIDs[0]].currency;
    }

    clearFiguresIncomeBalance();

    var selectedAccountsInfo = [];
    for (acc in accountsInfo) {
        if (accountIDs.includes(Number(acc))) {
            const account = accountsInfo[acc]
            selectedAccountsInfo.push(account);
            conversion = getConversionForAccount(account, selectedCurrency, conversionsDict);
            setFiguresIncomeBalance(account.balances, projectionTimescaleInMonths, conversion, selectedCurrency);
        }
    }

    calculate_dataset(selectedAccountsInfo, projectionTimescaleInMonths, selectedCurrency, conversionsDict);
}

function clearFiguresIncomeBalance() {
    document.getElementById('projectedIncomeNum').innerText = 0.00;
    document.getElementById('projectedTotalNum').innerText = 0.00;
}

function setFiguresIncomeBalance(balances, timescale, conversion, selectedCurrency) {
    timescale -= 1;
    const projectedIncomeNumText = document.getElementById('projectedIncomeNum');
    const projectedTotalNumText = document.getElementById('projecteTtotaNnum');
    const projectedIncomeCurrencyText = document.getElementById('projectedIncomeCurrency');
    const projectedTotalCurrencyText = document.getElementById('projectedTotalCurrency');

    let projectedIncomeNum = parseFloat(projectedIncomeNumText.innerText);
    let projectedTotalNum = parseFloat(projectedTotalNumText.innerText);

    projectedIncomeNum += parseFloat(conversion) * (parseFloat(balances[timescale]) - parseFloat(balances[0]));
    projectedTotalNum += parseFloat(conversion) * parseFloat(balances[timescale]);

    projectedIncomeCurrencyText.innerText = selectedCurrency;
    projectedTotalCurrencyText.innerText = selectedCurrency;
    projectedIncomeNumText.innerText = projectedIncomeNum.toFixed(2);
    projectedTotalNumText.innerText = projectedTotalNum.toFixed(2);
}