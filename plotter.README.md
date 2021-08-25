# Infograph plotter

The infograph plotter is an easy way to vivualise the data collected by the Ecocar-Unicamp telemetry sistem.
It takes the informaition from a serial comunication and shows it in realtime in the form of a line graph. 
It automates the entire process making it easy for the user. The plotter also has the possibility to selecte 
the data displayed and offers tools to analise specific data points for a more indepth analisies.

## Instalation

(instructions on how to install latest version)

The latest version finnished is: V.1.0

## Usage

### Connecting

To connect to the telemetry sistem click in the "connect" button. This will start the connecting process
indicated in the button.

<img src=> (add img)

When a connection is stablished the button will the button text will change to "connected".

<img src=> (add img)

### Navagating the graph

To best visualise the data the user can zoom in and out with the mouse wheel and walk trough the time exis 
with the right and left keys or with the bar on under the graph. By pressing the blue button you can change 
from live to static data. Passing the mouse cursor in the graph area will show the value of the closest points
that will be highlighted by dots on the data line.

<img src=> (add gif)

### Selecting infographs

The user can selecte what information to display clicking on the checkboxes on the right side of the window.
This selection will be saved in the current tab and new tabs can be opend with the "new tab" button. To change the
tab being shown just click the tab wich you want.

<img src=> (add gif)

## Code info

The plotter is write in python using the [pygame library](https://www.pygame.org/news) wich makes the graphic interface and user input easy to implement.
The [pyserial library](https://pyserial.readthedocs.io/en/latest/pyserial.html) is also used for the comunication with the telemetry system.
