## Manual Tests
Manual testing occurred regularly throughout local development. Tests are documented below.

### Homepage
|Test #|Test|Results|Evidence|
| --- | --- | --- | --- |
|1|**Navidation Bar** - adapts to screen size |Pass| Nav bar changes to toggle on smaller devices<br>
![Nav bar](static/images/non-login-user.png)<br>
![Nav bar small](static/images/mobile-non-login-user.png) |
|2|**Login/Register** button disappears when user is logged in |Pass| Register disappears when the user is logged in and appears if the user has not been authenticated. Registered/Logged in users can **Make Booking** and view **My Bookings**.<br>
![login](static/images/changes-login-registered.png)|
|3| Social links go to the correct external pages |Pass| All links were tested by clicking them, **Facebook, X, Instagram**. ![Socials](static/images/social-links.png)|
|4| clicking on **Services** within the navigation bar goes to the services page. The <em>browse services</em> link on the home page was also tested by clicking the link. |Pass| Clicking Services tab within Navigation Bar and Link on homepage. |
|5| Clicking **Make a Booking** takes the user to the booking form. **My Bookings** takes the user to any booked - Booking Details. So the user can view any bookings they made |Pass| By clicking either Make a Booking or My Bookings within the Navigation Bar. Make a Booking can also be accessed via Link on Homepage.<br>
![Homepage Links](static/images/links-homepage.png) |
|6| Logout directs the user to Signout confirmation page |Pass| By clicking Logout the user is asked to confirm if they wish to Sign Out .<br>
![Sign Out](static/images/signout-confirm.png) |


### Make a Booking
|Test #|Test|Results|Evidence|
| --- | --- | --- | --- |
|1| Booking Form **Validation** and **Error Handling** |Pass| All fields required before submit. Notes cannot accept just numbers, letters are also required, spacing allowed. <br>
![BookingForm](static/images/booking-validation.png)
![BookingForm](static/images/notes-bookingform.png)|
|2| Booking Form **accepts** booking and **redirects** the user to My Bookings |Pass| When the user fills in the Booking Form and clicks Book Now, the user is redirected to My Bookings, where they can view booking details, edit and delete their booking. <br>
![Confirmed](static/images/booking-confirmed.png)
![Details](static/images/booking-details.png)|
|3| User can **Edit** their booking by clicking edit. By Clicking edit the user can only change the appointment availability.|Pass| Availability is the only area of the form that can be amended, all other fields are shaded. <br>
![Edit](static/images/edit-booking.png)|
|4| User can **Cancel** their booking at any time. |Pass| By clicking the Cancel button and confirming cancellation. <br>
![contact](static/images/cancel-booking.png) |
|5| Slots that are booked, are **removed** from availability. |Pass| As above booking confirmed on the <em>1st of September, 09.00am to 09.30am</em>. On further booking attempt, this slot no longer exists. ![Slot Taken](static/images/slot-taken.png) |
|6| Slots that are **Amended(Edited)** are returned to Availability. |Pass| User clicks Edit, changes Booking Availability to <em>1st of September, 09.30am to 10.00am</em>, previous slot booked returns to availability. <br>
 ![Edited](static/images/booking-edited.png) ![Returned](static/images/returned-slot.png) |
|7| Slots that are **Cancelled** return to Available Slots. |Pass| User clicks Cancel, confirms Cancellation, is redirected to My Bookings and recieves confirmation message. <br>
![Cancel](static/images/booking-cancelled.png) ![All Slots Returned](static/images/all-slots-returned.png)|