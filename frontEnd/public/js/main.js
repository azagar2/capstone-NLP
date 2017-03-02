// user/event -> buttonCard, formCard, card
$(document).ready(function(){
  var users;
  var numEvents;
  $('#startDemoBtn').click(function(){
    $('html, body').animate({
       scrollTop: $('#userButtonCard').offset().top
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
  var userForm = `
  <div class="hidden col-2 offset-2" id="userFormCard">
    <div class="card add-user-card">
      <img src="../images/user_icon_${users.length + 1}.png" alt="User 1" class="circle-image">

      <div class="col-10 offset-1">
        <form action="">
          <input class="input-field" type="text" placeholder="User ${users.length + 1}" id="userNameField">

          <div class="select-style">
            <select id="userLocationField">
              <option value="Location 1">Location 1</option>
              <option value="Location 2">Location 2</option>
              <option value="Location 3">Location 3</option>
              <option value="Location 4">Location 4</option>
            </select>
          </div>

          <div class="button-pink" id="createUserBtn">Create</div>
        </form>
      </div>

    </div>
  </div>
  `
  $(`#userRow${users.length}`).prepend(userForm);
  $('#userFormCard').removeClass('hidden');
  $('#userFormCard').addClass('animated fadeInDown');
  $('#createUserBtn').on("click", createUserButton);
};

// =======================================================================================================

//called to create a user
function createUserButton(){
  var userName = $('#userNameField').val();
  var userLocation = $('#userLocationField').val();
  var newUser = `
  <div class="hidden col-2 offset-2" id="newUser${users.length}">
    <div class="card user-card">
      <img src="../images/user_icon_${users.length + 1}.png" alt="${userName}" class="circle-image"/>
      <hr class="horizontal-line"/>
      <div> ${userName} </div>
      <div> ${userLocation} </div>
    </div>
  </div>
  `;

  var addEventCard = getEventButtonCard(users.length);

  $('#userFormCard').remove();
  $(`#userRow${users.length}`).prepend(newUser);
  $(`#eventContainer${users.length}`).append(addEventCard);

  $(`#newUser${users.length}`).removeClass('hidden');
  $(`#newUser${users.length}`).addClass('animated fadeInDown');

  $(`#eventButtonCard${users.length}`).addClass('animated fadeInDown');
  $(`#eventButtonCard${users.length}`).removeClass('hidden');
  $(`#eventButtonCard${users.length}`).on("click", eventButtonCardFn);

  // //store user that was created
  users.push({name: userName, location: userLocation});

  //create row for new user
  var newUserRow = `
      <div class="ryan-row" id="userRow${users.length}">
        <div class="col-6 events-container" id="eventContainer${users.length}">
        </div>
      </div>
  `;
  $('.create-user-card-holder').append(newUserRow);

  var userButtonCard = `
  <div class="hidden col-2 offset-2" id="userButtonCard">
    <div class="card add-user-card">
      <div class="add-text">
        <span class="plus"> + </span> Add User
      </div>
    </div>
  </div>
  `

  $(`#userRow${users.length}`).prepend(userButtonCard);
  $('#userButtonCard').removeClass('hidden');
  $('#userButtonCard').addClass('animated fadeInDown');
  $('#userButtonCard').on("click", userButtonCardFn);
};

// =======================================================================================================

function eventButtonCardFn(){
  var eventId = `#${this.id}`;
  var row = eventId.split('').pop();

  var eventCardForm = `
  <div class="hidden col-6 remove-padding" id="eventFormCard${row}">
    <div class="card add-event-card">

      <div class="input-group event-search">
        <input type="text" class="form-control input" placeholder="Search Events" />
        <span class="input-group-btn">
          <button class="btn btn-info btn" type="button" id="eventSearchBtn${row}">
            <i class="glyphicon glyphicon-search"></i>
          </button>
        </span>
      </div>

      <div class="event-search-container" id="eventSearchContainer${row}">
        <!-- TODO: fill with events from db -->
      </div>

      <div class="button-pink" id="createEventBtn${row}">Create</div>
    </div>
  </div>
  `

  $(eventId).remove();
  $(`#eventContainer${row}`).append(eventCardForm);
  $(`#eventFormCard${row}`).removeClass('hidden');
  $(`#eventFormCard${row}`).addClass('animated fadeInDown');

  $(`#createEventBtn${row}`).on("click", createEventButton);
};

// =======================================================================================================

function createUserContinueBtn(){
  //inject recommendation page
  var recPage = `
  <div class="recommend-events-background">
    <h1 class='page-title'> Recommend Events </h1>

    <div class="ryan-row">
      <div class="button-group">
        <div class="button-pink"> Recommend </div>
      </div>
    </div>

    <div class="ryan-row">
      <div class="col-10 offset-1">
        <ul class="nav nav-tabs nav-justified">
          <li class="active"><a href="#u1" data-toggle="tab">User 1</a></li>
          <li><a href="#u2" data-toggle="tab">User 2</a></li>
          <li><a href="#u3" data-toggle="tab">User 3</a></li>
        </ul>
        <div class="tab-content" style="margin: 10px;">
          <div class="tab-pane active fade in" id="u1">
            user 1
          </div>
          <div class="tab-pane fade" id="u2">
            user 2
          </div>
          <div class="tab-pane fade" id=u3>
            user 3
          </div>
        </div>
      </div>
    </div>
  </div>
  `
  $('body').append(recPage);
  $('html, body').animate({
     scrollTop: $('.recommend-events-background').offset().top
   }, 1000);
};

// =======================================================================================================

function createEventButton(){
  var buttonId = `#${this.id}`;
  var row = buttonId.split('').pop();
  var eventCard = `
  <div class="hidden col-6 remove-padding" id="eventCard${numEvents}${row}">
    <div class="card add-event-card">
      Some new Event
    </div>
  </div>
  `

  $(`#eventFormCard${row}`).remove();
  $(`#eventContainer${row}`).append(eventCard);
  $(`#eventCard${numEvents}${row}`).removeClass('hidden');
  $(`#eventCard${numEvents}${row}`).addClass('animated fadeInDown');

  var addEventCard = getEventButtonCard(row);
  $(`#eventContainer${row}`).append(addEventCard);
  $(`#eventButtonCard${row}`).removeClass('hidden');
  $(`#eventButtonCard${row}`).addClass('animated fadeInDown');

  $(`#eventButtonCard${row}`).on("click", eventButtonCardFn);
  numEvents++;
};

// =======================================================================================================

function getEventButtonCard(row){
  var addEventCard = `
  <div class="hidden col-6 remove-padding"  id="eventButtonCard${row}">
    <div class="card add-event-card">
      <div class="add-text">
        <span class="plus"> + </span> Add Event
      </div>
    </div>
  <div>
  `
  return addEventCard;
};
