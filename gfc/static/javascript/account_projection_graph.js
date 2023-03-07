function loadInitialGraph(bankAccountsInfo, timeBands, conversions, mainCurrency) {
    try {
        getUserChoices(bankAccountsInfo, timeBands, conversions, mainCurrency);
    }
    catch(err) {
        calculateDataset(bankAccountsInfo, 12, timeBands, mainCurrency);
    }
}


function calculateDataset(accountsInfo, projectionTimescaleInMonths, timeBands, mainCurrency, selectedCurrency = "", conversionsDict = {}) {
    lineColours = [theme.primary, theme.secondary, theme.success, theme.warning, theme.danger, theme.dark]
    $(document).ready(() => {
        timeBands.length = projectionTimescaleInMonths;
        accountsDataset = [];
        for (account in accountsInfo) {
            accountsInfo[account].balances.length = projectionTimescaleInMonths;
            accountsDataset.push(getDatasetForAccount(accountsInfo[account], selectedCurrency, timeBands, lineColours[account % lineColours.length], conversionsDict, mainCurrency));
        }
        setChart(accountsDataset, timeBands, "Balance ("+selectedCurrency+")", "Months", "line");
    });
}
    

function getDatasetForAccount(account, selectedCurrency, timeBands, lineColour, conversionsDict, mainCurrency) {
    const conversion = getConversionForAccount(account, selectedCurrency, mainCurrency, conversionsDict)
    if (conversion != 1) {
        account.balances = account.balances.map(balance => balance * conversion);
    }

    return ({
        label: account.name,
        data: account.balances,
        backgroundColor: lineColour,
        borderColor: lineColour,
        borderWidth: 4
    });
}


function getConversionForAccount(account, selectedCurrency, mainCurrency, conversionsDict) {
    var conversion = 1;
    if (account.currency != selectedCurrency) {
      if (selectedCurrency == mainCurrency) {
        conversion = conversionsDict[account.currency];
      }
      else {
        conversion = conversionsDict[selectedCurrency];
        conversion = 1/conversion;
      }
    }
    return conversion
}


function roundToDecimalPlaces(element, dp) {
    element.value = parseFloat(element.value).toFixed(dp);
    if (dp == 0) {
      element.value = parseInt(element.value);
    }
}


function getUserChoices(accountsInfo, timeBands, conversionsDict, mainCurrency) {
    // Retrieves the user selection for the account and the projection timescale (in months)
    accountIDs = JSON.parse(document.getElementById('accountDropdown').value);
    const projectionTimescaleInMonths = document.getElementById('projectionTimescaleDropdown').value;
    const currencyChosen = document.getElementById('currencyDropdown').value;

    selectedCurrency = mainCurrency

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
            conversion = getConversionForAccount(account, selectedCurrency, mainCurrency, conversionsDict);
            setFiguresIncomeBalance(account.balances, projectionTimescaleInMonths, conversion, selectedCurrency);
        }
    }

    calculateDataset(selectedAccountsInfo, projectionTimescaleInMonths, timeBands, mainCurrency, selectedCurrency, conversionsDict);
}


function clearFiguresIncomeBalance() {
    document.getElementById('projectedIncomeNum').innerText = 0.00;
    document.getElementById('projectedTotalNum').innerText = 0.00;
}


function setFiguresIncomeBalance(balances, timescale, conversion, selectedCurrency) {
    timescale -= 1;
    const projectedIncomeNumText = document.getElementById('projectedIncomeNum');
    const projectedTotalNumText = document.getElementById('projectedTotalNum');
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