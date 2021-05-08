const requestSpreadSheetId = PropertiesService.getScriptProperties().getProperty('SPREAD_SHEET_ID');
const slackVerificationToken = PropertiesService.getScriptProperties().getProperty('SLACK_VERIFICATION_TOKEN');
const slackBotToken = PropertiesService.getScriptProperties().getProperty('SLACK_BOT_TOKEN');
const botPostUrl = PropertiesService.getScriptProperties().getProperty('SLACK_BOT_POST_URL');
const weekname = ["dummy","月","火","水","木","金","土","日"];
const eventname = {"ENTER": "入室", "LEAVE":"退室"}

function doPost(e) {
  var json = JSON.parse(e.postData.contents);
  appendData(json.data);
  sendToSlack(json.data);
  return ContentService.createTextOutput('success');
}

function appendData(data){
  let spreadSheetById = SpreadsheetApp.openById(requestSpreadSheetId);
  let d = new Date(data.datetime);
  let fdate = Utilities.formatDate(d, "JST", "YYYY/MM/dd (E) HH:mm");
  let date = d.getDate();
  let day = d.getDay();
  let diff = date - day - 2 + (day == 6 ? 8 : 1);
  let referenceDate = Utilities.formatDate(new Date(d.setDate(diff)), "JST", "YYYY/MM/dd (E)");
  let sheetByDate　= spreadSheetById.getSheetByName(referenceDate.toString());
  if(!sheetByDate){
    sheetByDate = spreadSheetById.insertSheet();
    sheetByDate.setName(referenceDate.toString());
    sheetByDate.getRange(1,1).setValue("日時");
    sheetByDate.getRange(1,2).setValue("入室/退室");
    sheetByDate.getRange(1,3).setValue("名前");
  }
  let lastRow = sheetByDate.getLastRow();
  sheetByDate.getRange(lastRow+1,1).setValue(fdate);
  sheetByDate.getRange(lastRow+1,2).setValue(eventname[data.event]);
  sheetByDate.getRange(lastRow+1,3).setValue(data.name);
}

function sendToSlack(data){  
  message = data.name + "さんが" + eventname[data.event] + "しました"

  let jsonData = {
    "username": 'ISLabBOT',
    "text": message
  };

  let payload = JSON.stringify(jsonData);
  
  let message_options = {
    "method" : "post",
    "contentType": "application/json",
    "payload" : payload
  };

  UrlFetchApp.fetch(botPostUrl, message_options);
}