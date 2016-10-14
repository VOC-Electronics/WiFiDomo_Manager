# WiFiDomo_Manager
======================
- Authors: Martijn van Leeuwen, Mano Biletsky
- Twitter: [@RaspberryPiNL]
- URL: [Website](http://www.voc-electronics.com)
- Email: [Martijn van Leeuwen](mailto:info@voc-electronics.com)
- Created: Jun 1st, 2016
- Version: 0.1

## Description
Een flask based interface for the WiFiDomo product line.


## Database:
* Currently we only use SQLite3 local database.
* Future release(s) might include the use of Postgress and/or MySQL/MariaDB/etc.


## Docker
* We now have a Dockerfile in the repo to launch the WifiDomo manager in your own
  Docker Container.
  

## Scheduling:

The Scheduling feature uses CRON.<br>
Be sure that the user running the WiFiDomo Manager has access to create/modify it's Crontab.<br>

Field Name |	Mandatory |	Allowed Values | Allowed Special Characters
------------ | ------------- | ------------- | -------------
Minutes 	   | Yes 	        | 0-59 	         | * / , -
Hours| 	     | Yes 	        | 0-23 	         | * / , -
Day of month | Yes 	        | 1-31 	         | * / , -
Month  	     | Yes 	        | 1-12 or JAN-DEC| * / , -
Day of week  | Yes 	        | 0-6 or SUN-SAT | * / , -

Supported special cases allow crontab lines to not use fields.<br> 
These are the official supported aliases, but are not yet available in this application:<br>

Case | Meaning
------------ | ------------
@reboot 	 | Every boot
@hourly 	 | 0 * * * *
@daily 	   | 0 0 * * *
@weekly 	 | 0 0 * * 0
@monthly 	 | 0 0 1 * *
@yearly 	 | 0 0 1 1 *
@annually  | 0 0 1 1 *
@midnight  | 0 0 * * *

## Branches
* origin/master - Master Branch
* origin/development - development branch


## Whishlist:


## Python and other required Libraries:
* Check the requirements.txt ;)

### Other required libraries:
* libssl-dev
* libffi


###possibly, if xml is needed:
* libxslt1-dev
* libxml2
* libxml2-dev


## DISCLAIMER

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Version History

* 0.5 - 
* 0.4 -
* 0.3 - 
* 0.2 - 
* 0.1 - Pre-Alpha (Only add/delete/modify wifidomos and locations work.)
* 0.0 - Initial code

