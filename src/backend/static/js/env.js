let DOMAIN = window.location.protocol + "//" + window.location.host;

let sequence1;
let sequence2;
let last_response = Date.now();  // unix timestamp in milliseconds

$(document).ready(function () {
  get_email();
  console.log(last_response);
});


function update_sequences(data) {
  console.log("updating sequences");
  console.log(data);

  data = JSON.parse(data);
  if (typeof data.error !== 'undefined') {
    alert(data.error);
  } else {
    $("#email_text").text(data.email);
  }
}

function get_email() {
  console.log("getting a new email");
  $.get("/getemail", function (data) {
    update_sequences(data);
  })
    .fail(function (error) {
      alert("ERROR");
    })
}

function no_response_checker() {
  console.log("Beginning no-response-checker...");
  setTimeout(function () {
    diff = Date.now() - last_response;
    console.log("Its been some time, diff: " + diff);
    if (diff > 1999) {
      // alert("The server took too long to respond!");
    }
  }, 2000);
}

function send_preference(feedback) {
  last_response = Date.now();
  no_response_checker();
  $.ajax({
    type: "POST",
    url: "/feedback",
    data: JSON.stringify({feedback: feedback}),
    contentType: "application/json; charset=utf-8",
    success: function (data) {
      last_response = Date.now();
      update_sequences(data);
    },
    failure: function (errMsg) {
      console.log("failed to send feedback");
      get_email();
    }
  });
}

function left_clicked() {
  send_preference(-1);
}

function center_clicked() {
  send_preference(0);
}

function right_clicked() {
  send_preference(1);
}