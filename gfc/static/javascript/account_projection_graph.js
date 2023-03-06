function loadInitialGraph() {
    try {
        getUserChoices();
    }
    catch(err) {
        const accountsInfo = JSON.parse("{{bank_account_infos|escapejs}}");
        calculateDataset(accountsInfo, 12)
    }
}

function calculateDataset(accountsInfo, projectionTimescaleInMonths, selectedCurrency = "{{main_currency}}", conversionsDict = JSON.parse("{{conversion_to_main_currency_JSON|escapejs}}")) {
    lineColours = [theme.primary, theme.secondary, theme.success, theme.warning, theme.danger, theme.dark]
    $(document).ready(() => {
        var timeBands = {{timescales_strings|safe}};
        timeBands.length = projectionTimescaleInMonths;
        accountsDataset = [];
        for (account in accountsInfo) {
            accountsInfo[account].balances.length = projectionTimescaleInMonths;
            accountsDataset.push(getDatasetForAccount(accountsInfo[account], selectedCurrency, timeBands, lineColours[account % lineColours.length], conversionsDict));
        }
        setChart(accountsDataset, timeBands, "Balance ("+selectedCurrency+")", "Months", "line");
    });
}
    
function getDatasetForAccount(account, selectedCurrency, timeBands, lineColour, conversionsDict) {
    const conversion = getConversionForAccount(account, selectedCurrency, conversionsDict)
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

function getConversionForAccount(account, selectedCurrency, conversionsDict) {
    var conversion = 1;
    if (account.currency != selectedCurrency) {
      if (selectedCurrency == '{{main_currency}}') {
        conversion = conversionsDict[account.currency];
      }
      else {
        conversion = conversionsDict[selectedCurrency];
        conversion = 1/conversion;
      }
    }
    return conversion
}