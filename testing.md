## Manual Tests
Manual testing occurred regularly throughout local development. Tests are documented below.

### index
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
|6| Booking Form **Validation** and **Error Handling** |Pass| All fields required before submit. Notes cannot accept just numbers, letters are also required, spacing allowed. <br>
![BookingForm](static/images/booking-validation.png) <br>
![BookingForm](static/images/notes-bookingform.png)
|
|8| Account status shows the correct position on the progress bar|Pass| when the user publishes a recipe the bar moves the correct percentage <br> ![profile 2](readme-media/manual_tests/index/profile_2.png)|
|9| Account status shows the correct colour of award|Pass| the colour of the status and the text of the status changes depending on how many recipes the user has made. <br> ![profile 2](readme-media/manual_tests/index/profile_2.png)|
|10| contact link navigates to the contact form on the about page|Pass| when the contact button is pressed it navigate to the about us page and uses an anchor to go down to the contact form <br> ![contact](readme-media/manual_tests/index/contact.png) |
|11| recipe card has a shadow when higlighted for ux|Pass| When the user highlight over a recipe a shadow behind it appears to make these experience better

![highlighted](readme-media/manual_tests/index/shadow.png) |
### about_us
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| contact form has the correct validation|Pass| a user can only send a message when all the relevant fields have been completed|
|2| contact form send email to the admin|Pass| when the user submit the contact form and email appears in the admin inbox|

![contact](readme-media/manual_tests/index/contact.png)
### logged_in_user_card
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| shows the right information for the user page that you were looking at|Pass| the links and the URL is display the correct user and details about the user|
|2| shows the correct colour status for the user|Pass| the status award of the user matches the correct phrase for example a user with 20 recipes will have a silver account|
|3| follow button appears if you are logged in and not following a user|Pass| the follow button shows the correct status depending if you are following I'm not following the user. if you are not logged in the bottom does not sure|
|4| button goes to a mini version showing a icon instead of Word when the screen is on a smaller view|Pass| if you are viewing the page on a mobile device instead of saying following or Unfollow it shows a font awesome icon|

![user card](readme-media/manual_tests/logged_in_user_card/follow_2.png)
### recipe_detail
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| if user is logged in it shows the edit button on their recipes|Pass| edit button only shows up if you are the author of the recipe|
|2| if user is logged in but not on the recipe the edit button does not appear|Pass|edit button only shows up if you are the author of the recipe|
|3| only if the user is logged in can they make a rating|Pass| the rating feature only works if you are authenticated and logged in|
|4| the print button shows the print dialogue so the user can print the recipe|Pass| the print button allows you to open up a print dialogue|
|5| only if user is logged in can they favourite a recipe|Pass| the favourite heart button only works if the user is authenticated|
|6| only if a user is logged in can they upload a image|Pass| upload image button is only visible if you are logged in and authenticated|
|7| a user that has uploaded a image can delete their own image|Pass| a user can only delete the image if they are the person who uploaded the image|
|8| images show on the recipe|Pass| what an image is uploaded it is shown on the correct recipe page|
|9| user can turn on and off comments|Pass| the comment button allows user to toggle on and off the comments linked to that recipe|
|10| only a log in user can leave a comment|Pass| the comment form is only visible when the user is logged in and authenticated|
|11| if the user has written a comment they can only delete their own comment|Pass| a log in authenticated user can only delete a comment that they have made|
|12| header image disappears when the user is on a smaller screen|Pass| the recipe header changes depending on the view size|
|13| splide images change how many are on screen depending on the view size|Pass| the slide feature displays the recipes and users depending on the view size|

![user edit button](readme-media/manual_tests/recipe_details/edit_buttton.png)
![user heading](readme-media/manual_tests/recipe_details/edit_heading.png)
![comments](readme-media/manual_tests/recipe_details/comments.png)
![image upload](readme-media/manual_tests/recipe_details/image_upload.png)
![rating](readme-media/manual_tests/recipe_details/rating.png)
![like](readme-media/manual_tests/recipe_details/like_button.png)
![print](readme-media/manual_tests/recipe_details/print_button.png)
### recipes
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| links go to the correct pages|Pass|All links were tested by clicking them|
|2| recipes link to the correct recipes|Pass|All links were tested by clicking them|
|3| the page pagination works|Pass|the pagination for the recipes shows correctly|
|4| sort and filter show results in the correct order|Pass| the sort and filter options were tested and showed the correct results|
|5| search shows the correct recipes|Pass| the search function shows the correct recipes|

![recipe 1](readme-media/manual_tests/recipes/recipe_icons.png)
![filter](readme-media/manual_tests/recipes/recipe_filter.png)
### user_favourites
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| recipes link to the correct recipe pages|Pass|All links were tested by clicking them|
|2| Page pagination works correctly|Pass|the pagination for the recipes shows correctly|

![likes 1](readme-media/manual_tests/user_favourites/likes_1.png)
### user_followers
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| correct users are shown in the following pages|Pass| the correct users were shown on the correct following pages|
|2| correct user rating is shown on the page|Pass| the correct rating was calculated|

![follows 1](readme-media/manual_tests/user_followers/follows_1.png)
### user_profile_page
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| user can edit account if they are on their own account|Pass| the edit account button is only shown if you are on the account proile page of the account you are logged in as|
|2| edit account shows a following or follow button if you are logged in|Pass| if you are not on your own profile page it shows if you are following or not following that user|
|3| splide changes size depending on how big the view is|Pass| the correct number of items are shown when the view size is changed|
|4| all links go to the correct pages|Pass|All links were tested by clicking them|

![profile 1](readme-media/manual_tests/user_profile_page/profile.png)
![profile 2](readme-media/manual_tests/user_profile_page/profile_2.png)
### user_recipe_add
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| the form has the correct validation|Pass| the form needs all required fields to be complete before it is submitted|
|2| sign postage is shown at the top of the form|Pass| there are clear instructions on how to add a new ingredient and how to write a new method for a recipe|

![add recipe 1](readme-media/manual_tests/user_recipe_add/recipe_form.png)
### user_recipes_edit
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| knows if the recipe is published or not|Pass| there is a clear green or red text to show the user if the recipe is published or hidden|
|2| shows what ingredients are verified|Pass| the recipes that are not verified show a white symbol or underlined|
|3| ingredient pagination works correctly|Pass| the pagination for the ingredients works correctly when the user searches for them|
|4| add an ingredient button only appears when less than 10 items show up in the search|Pass| when searching for an ingredient when the search results is are less than 10 it will show the user a button/option to add a new ingredient because it is not in the database|

![edit recipe 1](readme-media/manual_tests/user_recipe_edit/edit_recipe_1.png)
![edit recipe 2](readme-media/manual_tests/user_recipe_edit/edit_recipe_2.png)
![edit recipe 3](readme-media/manual_tests/user_recipe_edit/edit_recipe_3.png)
![edit recipe 4](readme-media/manual_tests/user_recipe_edit/edit_recipe_4.png)
### user_recipes
|Test #|Test|Results|Evidence|
| --- | --- | --- |--- |
|1| recipes link to the correct recipe pages|Pass|All links were tested by clicking them|
|2| Page pagination works correctly|Pass| the pagination for the recipes shows correctly|
|3| shows a colour around the recipe if it has been published or not only if you are logged in to your recipes|Pass| a green box is shown if a recipe has been published a read books is so if it is hidden|

![colour ring](readme-media/manual_tests/user_recipes/colour_box.png)
![colour box](readme-media/manual_tests/user_recipes/recipes_box.png)
***