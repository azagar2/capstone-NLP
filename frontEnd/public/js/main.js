$(document).ready(function(){
  var users;
  var numEvents;
  $('#startDemoBtn').click(function(){
    $('html, body').animate({
       scrollTop: $('#create-users-title').offset().top
     }, 1000);
  });

  $('#userButtonCard').on("click", userButtonCardFn);
  $('#createUserContinueBtn').on("click", createUserContinueBtn);

  // Handle window resizing
  $(window).resize(function() {
    console.log($(window).width());
  });
});

// =======================================================================================================

//called to render the form
function userButtonCardFn(){
  if(typeof(users) === "undefined"){ users = []; numEvents = 0;}

  $('#userButtonCard').remove();
  var userForm = getUserFormCard(users.length + 1);
  $(`#userRow${users.length}`).prepend(userForm);
  fadeInAnimate('userFormCard')
  $('#createUserBtn').on("click", createUserButton);
};

// =======================================================================================================

//called to create a user
function createUserButton(){
  var userName = $('#userNameField').val() || `User ${users.length + 1}`;
  var userLocation = $('#userLocationField').val();

  var newUser = `
  <div class="hidden col-2 offset-2" id="newUser${users.length}">
    <div class="card user-card">
      <img src="../images/user_icon_${users.length + 1}.png" alt="${userName}" class="circle-image"/>
      <hr class="horizontal-line"/>
      <div> ${userName} </div>
      <div> ${userLocation} </div>
      <div><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></div>
    </div>
  </div>
  `;

  var addEventCard = getEventButtonCard(users.length);

  $('#userFormCard').remove();
  $(`#userRow${users.length}`).prepend(newUser);
  $(`#eventContainer${users.length}`).append(addEventCard);

  fadeInAnimate(`newUser${users.length}`);
  fadeInAnimate(`eventButtonCard${users.length}`);

  $(`#eventButtonCard${users.length}`).on("click", eventButtonCardFn);

  // //store user that was created
  users.push({name: userName, location: userLocation});
  users[users.length - 1]["events"] = [];

  //create row for new user
  var newUserRow = `
    <hr class="horizontal-line" style="width: 50%;"/>
      <div class="ryan-row" id="userRow${users.length}">
        <div class="col-6 events-container" id="eventContainer${users.length}">
        </div>
      </div>
  `;
  $('.create-user-card-holder').append(newUserRow);

  var userButtonCard = `
  <div class="hidden col-2 offset-2" id="userButtonCard">
    <div class="card add-user-card card-hover">
      <div class="add-text">
        <span class="plus"> + </span> Add User
      </div>
    </div>
  </div>
  `

  $(`#userRow${users.length}`).prepend(userButtonCard);
  fadeInAnimate("userButtonCard");
  $('#userButtonCard').on("click", userButtonCardFn);
};

// =======================================================================================================

function eventButtonCardFn(){
  var eventId = `#${this.id}`;
  var row = eventId.split('').pop();

  var eventCardForm = getEventFormCard(row);

  $(eventId).remove();
  $(`#eventContainer${row}`).append(eventCardForm);
  fadeInAnimate(`eventFormCard${row}`);
  $(`#eventSearchBtn${row}`).on("click", searchEvents);
};

// =======================================================================================================

function createUserContinueBtn(){
  //inject recommendation page
  var recPage = `
  <div class="recommend-events-background">
    <h1 class='page-title white'> Recommend Events </h1>

    <div class="ryan-row" style=''>
      <div class="col-10 offset-1">
        <div class="col-2" style="margin-top: 50px;">
          <ul class="nav nav-tabs">
            <li class="active tab-item"><a href="#a1" data-toggle="tab"> ${users[0].name}</a></li>`

  for(var i = 1; i<=users.length-1; i++){
    recPage = recPage.concat(`<li class="tab-item"><a href="#a${i+1}" data-toggle="tab"> ${users[i].name}</a></li>`);
  }

  recPage = recPage.concat(`
        </ul>
      </div>
      <div class="tab-content col-10">
        <div class="rec-subheader col-2"> Past Events</div>
        <div class="col-2 offset-7" id="theRecBtn"> Recommend </div>`);


  for(var i = 0; i<=users.length-1; i++){
    recPage = recPage.concat(`<div class="tab-pane" id="a${i+1}">
    <div class="events-container" style="width:90%; height: 260px;" id="b${i+1}"></div></div>`);
  }

  recPage = recPage.concat(`</div> </div> </div> </div> </div> </div>`);

  if(!$(`.recommend-events-background`).length){
    $('body').append(recPage);
    $('#theRecBtn').on("click", recommendEvents);
    $('#a1').addClass("active fade in");
    for(var i = 0; i<=users.length-1; i++){
      for(var j=0; j<=users[i]["events"].length-1; j++){
        getEventCard(users[i]["events"][j], `b${i+1}`);
        numEvents++;
      }
      $(`#a${i+1}`).append(`
        <hr class="horizontal-line col-6 offset-3" style="padding: 0px;"/>
        <div class="events-container" style="width:100%; height: 260px;" id="c${i+1}"></div>`);
    }
  }

  $('html, body').animate({
     scrollTop: $('.recommend-events-background').offset().top
   }, 1000);
};

// =======================================================================================================

function createEventButton(){
  var jq = $(`#${this.id}`);
  var row = jq.data("row");
  var eventData = { title: jq.text(), id: this.id, description: jq.data("description"), category: jq.data("category"), price: jq.data("price"), image: jq.data("image"), cover_photo: jq.data("cover_photo") }
  getEventCard(eventData, `eventContainer${row}`);

  $(`#eventFormCard${row}`).remove();
  // $(`#eventContainer${row}`).append(eventCard);
  $(`#eventCard${numEvents}`).addClass("hidden");
  fadeInAnimate(`eventCard${numEvents}`);

  var addEventCard = getEventButtonCard(row);
  $(`#eventContainer${row}`).append(addEventCard);
  fadeInAnimate(`eventButtonCard${row}`);

  $(`#eventButtonCard${row}`).on("click", eventButtonCardFn);

  if(users[row]){
    users[row]["events"].push(eventData);
    numEvents++;
  }
};

// =======================================================================================================

function searchEvents(){
  var row = this.id.split("").pop();
  var searchVal = $(`#event-search${row}`).val().toUpperCase();
  $(`#eventSearchContainer${row}`).empty();

  $.getJSON( "../data/pastEvents.json", function( data ) {
    var items = [];
    $.each( data, function(k,v) {
      if(v.title.toUpperCase().includes(searchVal) || v.description.toUpperCase().includes(searchVal) || v.category.toUpperCase().includes(searchVal)){
        items.push( `<div data-row="${row}" data-description="${v.description}" data-category="${v.category}"
          data-price="${v.price}" data-image="${v.image}" data-cover_photo="${v.cover_photo}" class="event-listing" id="${v.id}"> ${v.title} </div>` );
      }
    });
    $(`#eventSearchContainer${row}`).append(items.join(""));

    $.each($(`.event-listing`), function(k, v){
      if(`#${v.id}` !== "#"){
        $(`#${v.id}`).on("click", createEventButton);
      }
    });
  });
};

// =======================================================================================================

function fadeInAnimate(id){
  $(`#${id}`).removeClass('hidden');
  $(`#${id}`).addClass('animated fadeInDown');
}

function recommendEvents(){
  var w = $(".tab-pane.active").attr("id").split("").pop();
  // var w = this.id.split("").pop();
  var ids = $.map(users[w-1]["events"], function(val) { return val.id; });
  if(ids[0]) var e1 = `event1=${ids[0]}`;
  if(ids[1]) var e2 = `&event2=${ids[1]}`;
  if(ids[2]) var e3 = `&event3=${ids[2]}`;

  var url = `http://localhost:3001/api/v1/recommendations/user?${e1 || ""}${e2 || ""}${e3 || ""}`;
  console.log(url);
  $.get(url, function(data, status){
    // console.log(data);
    $.each(data[0].slice(0,9), function(j){
      $.getJSON("../data/futureEvents.json", function(json){
        $.each(json, function(k, v){
          if(v.id == data[0][j]){
            getEventCard(v, `c${w}`);
            numEvents++;
          }
        });
      });
    });
  });

}

// ==============  GETTERS =======================
function getEventCard(eventObject, id){
  $(`#${id}`).append(`
       <div class="col-5 remove-padding" id="eventCard${numEvents}">
         <div class="card event-card">

           <div class="bg" style="background-image: url('${eventObject.cover_photo}')">
             <div class="events-title"> ${eventObject.title} </div>
           </div>

           <div class="events-content">
             <div><img class="events-img-small pull-left" src="${eventObject.image}"></div>
             <div class="events-description"> ${eventObject.description} </div>
             <div style="display:inline-flex; margin-top: 10px;">
               <span class="glyphicon glyphicon-trash events-trash" aria-hidden="true"></span>
               <div>|</div>
               <div class="events-category"> ${eventObject.category} </div>
               <div>|</div>
               <div class="events-price"> $${eventObject.price} </div>
             </div>
           </div>

         </div>
       </div>
  `);
};

// =======================================================================================================

function getEventButtonCard(row){
  return(`
  <div class="hidden col-5 remove-padding"  id="eventButtonCard${row}">
    <div class="card event-card card-hover">
      <div class="add-text">
        <span class="plus"> + </span> Add Event
      </div>
    </div>
  <div>
  `);
};

function getEventFormCard(row){
  return (`
    <div class="hidden col-5 remove-padding" id="eventFormCard${row}">
    <div class="card event-card">

      <div class="input-group event-search">
        <input id="event-search${row}" type="text" class="form-control input" placeholder="Search Events" />
        <span class="input-group-btn">
          <button class="btn btn-info btn" type="button" id="eventSearchBtn${row}">
            <i class="glyphicon glyphicon-search"></i>
          </button>
        </span>
      </div>

      <div class="event-search-container" id="eventSearchContainer${row}">
        <!-- TODO: fill with events from db -->
      </div>

    </div>
  </div>
  `)
}

function getUserFormCard(l){
  return (`
  <div class="hidden col-2 offset-2" id="userFormCard">
    <div class="card add-user-card">
      <img src="../images/user_icon_${l}.png" alt="User 1" class="circle-image">

      <div class="col-10 offset-1">
        <form action="">
          <input class="input-field" type="text" placeholder="User ${l}" id="userNameField">

          <div class="select-style">
            <select id="userLocationField">
              <option value="Location 1">Location 1</option>
              <option value="Location 2">Location 2</option>
              <option value="Location 3">Location 3</option>
              <option value="Location 4">Location 4</option>
            </select>
          </div>

          <div class="button-pink" id="createUserBtn" style="width: 100%; margin-left: 2px; margin-top: 4px;">Create</div>
        </form>
      </div>

    </div>
  </div>
  `);
};
