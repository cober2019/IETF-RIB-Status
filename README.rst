
.. image:: https://travis-ci.com/cober2019/IETF-RIB-Status.svg?token=Jd38SqdR7ErpxMoqVxEQ&branch=main
    :target: https://travis-ci.com/cober2019/IETF-RIB-Status
.. image:: https://img.shields.io/badge/NETCONF-required-blue
    :target: -

IETF-RIB-Status
================

    IETF RIB Status allows you to view your current RIB table as well as poll the table and compare to previous. Any entries that are flapping will be displayed
    on the screen without reloading the page.
    
**Notes**
    
    - On intial login and page refreshes the page may take some time to load. This is due to fetching data from the device.
    - You will notice 'Scanning...' and ''Fetching" status messages to show program activity.
    - The program may have issues with cisco switches as the response time to get the RIB is very slow. Still don't hesitate to try!
    - Testing was done with ASR and ISR. I haven't tried with any other vendor devices. Please let me know the results if you try (cober91130@gmail.com)
    - Please run requirements.txt before using this program
    - Access using http://{your_local_ip}:5000
    - Clone using git clone https://github.com/cober2019/IETF-RIB-Status.git (Linux: cd IETF-RIB-Status-->pip install -r requirements.txt-->python run.py)
    
**YANG Model:**
---------------
    **IETF-Routing:** (https://tools.ietf.org/html/rfc8349)

**Login:**
---------
   - IP Address should be whatever IP you use to manage the device
   - NETCONF port is default 830.
   
.. image:: https://github.com/cober2019/IETF-RIB-Status/blob/main/images/Login.PNG
    :target: -

**Protocols:**
--------------

.. image:: https://github.com/cober2019/IETF-RIB-Status/blob/main/images/Protocols.PNG
    :target: -
    
**RIB w/ Flapping Entries:**
----------------------------

.. image:: https://github.com/cober2019/IETF-RIB-Status/blob/main/images/RoutesFlapping.PNG
    :target: -

