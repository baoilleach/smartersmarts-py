var MAXHITS = 50;

function myencode(text) {return encodeURIComponent(text);}
function mydecode(text) {return text;}

var SNSRouter = Backbone.Router.extend({

  routes: {
    "search/:smarts/": "search",
  },

  search: function(smarts) {
    var decoded = mydecode(smarts);
    UpdateImages(smarts);
    if ($('#entrybox').val() != decoded) {
      $('#entrybox').val(decoded);
    }
  }

});

function Initialize()
{
  var typingTimer;

  // Add behaviour to text area
  $('#entrybox').on("change keyup paste", function() {
    clearTimeout(typingTimer);
    var doneTypingInterval = 1000;
    typingTimer = setTimeout(function(){app.navigate("search/"+myencode($('#entrybox').val())+"/", {trigger: true});},
                             doneTypingInterval);
  });
  $('#entrybox').on('keydown', function () {
    clearTimeout(typingTimer);
  });
}

$(function() {
  app = new SNSRouter();
  Backbone.history.start();

  Initialize();
});

function HandleInvalid()
{
  $('#dv_png').addClass("limbo");
  $('#entryform').removeClass("has-success").addClass("has-warning");
  $('#entryboxicon').removeClass("glyphicon-ok").addClass("glyphicon-remove");
}

function HandleNoMatches()
{
  $('#dv_png').html("<p>No matches found</p>");
  $('#entryform').removeClass("has-warning").addClass("has-success");
  $('#entryboxicon').removeClass("glyphicon-remove").addClass("glyphicon-ok");
}

function HandleMatches(matches)
{
  var mhtml = [];
  $.each(matches, function(idx, smi) {
    if (idx == MAXHITS) {
      mhtml.push('<div>[showing top ' + MAXHITS + ' of ' + matches.length + ']</div>');
      return false;
    } else {
      mhtml.push('<img src="https://compchem.soseiheptares.com/depict/depict/bow/png?abbr=off&disp=bridgehead&showtitle=true&annotate=colmap&smi=' + myencode(smi) + '" />\n')
    }
  });
  $('#dv_png').html(mhtml.join('')).removeClass("limbo");
  $('#entryform').removeClass("has-warning").addClass("has-success");
  $('#entryboxicon').removeClass("glyphicon-remove").addClass("glyphicon-ok");
}

function HandleSearch() {
  $('#entryboxicon').removeClass("glyphicon-remove").removeClass("glyphicon-ok");
  $('#dv_png').addClass("limbo");
}


function IsInvalidQuick(smarts)
{
  var paren = 0;
  var bracket = 0;
  for (var i=0; i<smarts.length; ++i) {
    switch(smarts[i]) {
      case '[': bracket++; break
      case ']': bracket--; break
      case '(': paren++; break;
      case ')': paren--; break;
    }
  }
  return (bracket!=0 || paren!=0);
}

function UpdateImages(smarts)
{
  if (IsInvalidQuick(smarts)) {
    HandleInvalid();
    return;
  }

  HandleSearch();
  if(typeof ajax_request !== 'undefined')
    ajax_request.abort(); // Cancel any outstanding AJAX request
  ajax_request = $.ajax({
    dataType: "json",
    // type: "POST", // Use this to avoid caching
    type: "GET",
    url: '/smartsrefine/search',
    data: {"smarts": smarts},
  }).done(function(data) {
    var isvalid = data["valid"];
    if (!isvalid) {
      HandleInvalid();
      return;
    }
    var matches = data["matches"];
    if (matches.length == 0) {
      HandleNoMatches();
      return;
    }
    HandleMatches(matches);
  });
}
