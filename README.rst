
.. image:: https://travis-ci.com/cober2019/IETF-RIB-Status.svg?token=Jd38SqdR7ErpxMoqVxEQ&branch=main
    :target: https://travis-ci.com/cober2019/IETF-RIB-Status
.. image:: https://img.shields.io/badge/NETCONF-required-blue
    :target: -

IETF-RIB-Status
================

    IETF RIB Status allows you to view your current RIB table as well as poll the table and compare to previous. Any entries that are flapping will be displayed
    on the screen without reloading the page.
    
**Notes**
    - On intial login and page reshreshes the page may take some time to load. This is due to fetching data from the device.
    - The program may have issues with cisco switches as the response time to get the RIB is very slow. Still don't hesitate to try!
    - Testing was dont with ASR and ISR. I havnt tried with any other vendor device. Please let me know the results if you try (cober91130@gmail.com)
    
**YANG Model:**
---------------
    **IETF-Routing:** (https://tools.ietf.org/html/rfc8349)

**Login:**
---------
    
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

