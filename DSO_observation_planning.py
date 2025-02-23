"""
===================================================================
Solveigh's customized DSO observation planning based on

https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html
https://github.com/yetanothergithubaccount/ObsPi

Some DSOs found in catalogues like
- the classical Messier catalogue
- Orphaned Beauties: https://www.astrobin.com/in2ev8/
- Faint Giants: https://www.astrobin.com/0unmpq/

python3 DSO_observation_planning.py --dso M31 --best # find best time and date to observe M31

python3 DSO_observation_planning.py --best

Determining and plotting the altitude/azimuth of a celestial object per day.
The results will be fixed in a json-file per day for quick reference.
Supplying a favorite direction (N, E, S, W) and a minimal altitude will
result in a list of matching DSOs from the internal catalogue.

--best/-b: determining approximately the best observation time and date per year,
           taking the moon phase/location into account
===================================================================

*Based on developments by: Erik Tollerud, Kelle Cruz*
*License: BSD*
"""

# sudo pip3 install astropy --break-system-packages
# sudo pip3 install astroquery --break-system-packages
# sudo pip3 install skyfield --break-system-packages
# sudo pip3 install pandas --break-system-packages
# sudo pip3 install suntime --break-system-packages
# sudo pip3 install pyephem --break-system-packages
# sudo pip3 install spaceweather--break-system-packages
# sudo pip3 install matplotlib-label-lines --break-system-packages

import os, sys, platform
import optparse
import matplotlib.pyplot as plt
import numpy as np
import datetime
from astropy.visualization import astropy_mpl_style, quantity_support
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from astroquery.simbad import Simbad # https://github.com/astropy/astroquery
import config # own
import sky_utils # own
import pytz

debug = False #True
base_dir = "./"

parser = optparse.OptionParser()
parser.add_option('-d', '--dso',
    action="store", dest="dso",
    help="Deep space object to check (M1, ...)") #, default="M31")
parser.add_option('-a', '--latitude',
    action="store", dest="latitude",
    help="Latitude", default=config.coordinates['latitude'])
parser.add_option('-o', '--longitude',
    action="store", dest="longitude",
    help="Longitude", default=config.coordinates['longitude'])
parser.add_option('-e', '--elevation',
    action="store", dest="elevation",
    help="Elevation (height)", default=config.coordinates['elevation'])
parser.add_option('-l', '--location',
    action="store", dest="location",
    help="Location", default=config.coordinates['location'])
parser.add_option('-f', '--debug',
    action="store_true", dest="debug",
    help="Debug mode", default=False)

parser.add_option('-b', '--best',
    action="store_true", dest="best",
    help="Check visibility during the year to find best date and time", default=False)

parser.add_option('-t', '--tonight',
    action="store_true", dest="tonight",
    help="Check visibility of DSOs tonight to find best time", default=False)
parser.add_option('-m', '--moon',
    action="store_true", dest="moon",
    help="Consider moon (illumination, location) during tonights checks.", default=False)
parser.add_option('-j', '--justthetopones',
    action="store_true", dest="justthetopones",
    help="Check visibility of DSOs tonight to find best time, consider the TOP ones only (requires tonight and moon option).", default=False)
parser.add_option('-r', '--direction',
    action="store", dest="direction",
    help="Filter tonight's best results for a certain direction (requires tonight and moon option).") # S/W/N/E

options, args = parser.parse_args()

if debug:
  print("Find best tonight's DSOs: " + str(options.tonight))
  print("Consider moon: " + str(options.moon))
  print("  display only the TOP ones: " + str(options.justthetopones))
  print("  filter for direction: " + str(options.direction))

if options.latitude:
  latitude = options.latitude

if options.longitude:
  longitude = float(options.longitude)

if options.elevation:
  elevation = int(options.elevation)

if options.location:
  location = options.location

if options.dso:
  dso_name = str(options.dso).upper()
else:
  dso_name = str("M31")

today = datetime.date.today()
theDate = today.strftime("%d.%m.%Y")

if options.debug:
  debug = True

my_DSO_list = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30", "M31", "M32", "M33", "M34", "M35", "M36", "M37", "M38", "M39", "M40", "M41", "M42", "M43", "M44", "M45", "M46", "M47", "M48", "M49", "M50", "M51", "M52", "M53", "M54", "M55", "M56", "M57", "M58", "M59", "M60", "M61", "M62", "M63", "M64", "M65", "M66", "M67", "M68", "M69", "M70", "M71", "M72", "M73", "M74", "M75", "M76", "M77", "M78", "M79", "M80", "M81", "M82", "M83", "M84", "M85", "M86", "M87", "M88", "M89", "M90", "M91", "M92", "M93", "M94", "M95", "M96", "M97", "M98", "M99", "M100", "M101", "M102", "M103", "M104", "M105", "M106", "M107", "M108", "M109", "M110", "NGC7822", "SH2-173", "NGC210", "IC63", "SH2-188", "NGC613", "NGC660", "NGC672", "NGC918", "IC1795", "IC1805", "NGC1055", "IC1848", "SH2-200", "NGC1350", "NGC1499", "LBN777", "NGC1532", "LDN1495", "NGC1555", "NGC1530", "NGC1624", "NGC1664", "Melotte15", "vdb31", "NGC1721", "IC2118", "IC410", "SH2-223", "SH2-224", "IC434", "SH2-240", "LDN1622", "SH2-261", "SH2-254", "NGC2202", "IC443", "NGC2146", "NGC2217", "NGC2245", "SH2-308", "NGC2327", "SH2-301", "Abell21", "NGC2835", "Abell33", "NGC2976","Arp316", "NGC3359", "Arp214", "NGC4395", "NGC4535", "Abell35", "NGC5068", "NGC5297", "NGC5371", "NGC5364", "NGC5634", "NGC5701", "NGC5963", "NGC5982", "IC4592", "IC4628", "Barnard59", "SH2-003", "Barnard252", "NGC6334", "NGC6357", "Barnard75", "NGC6384", "SH2-54", "vdb126", "SH2-82", "NGC6820", "SH2-101", "WR134", "LBN331", "LBN325", "SH2-112", "SH2-115", "LBN468", "IC5070", "vdb141", "SH2-114", "vdb152", "SH2-132", "Arp319", "NGC7497", "SH2-157", "NGC7606", "Abell85", "LBN 564", "SH2-170", "LBN603", "LBN639", "LBN640", "LDN1333", "NGC1097", "LBN762", "SH2-202", "vdb14", "vdb15", "LDN1455", "vdb13", "vdb16", "IC348", "SH2-205", "SH2-204", "Barnard208", "Barnard7", "vdb27", "Barnard8", "Barnard18", "SH2-216", "Abell7", "SH2-263", "SH2-265", "SH2-232", "Barnard35", "SH2-249", "IC447", "SH2-280", "SH2-282", "SH2-304", "SH2-284", "LBN1036", "NGC2353", "SH2-310", "SH2-302", "Gum14", "Gum15", "Gum17", "Abell31", "SH2-1", "SH2-273", "SH2-46", "SH2-34", "IC4685", "SH2-91", "Barnard147", "IC1318", "LBN380", "Barnard150", "LBN552", "SH2-119", "SH2-124", "Barnard169", "LBN420", "SH2-134", "SH2-150", "LDN1251", "LBN438", "SH2-154", "LDN1218", "SH2-160", "SH2-122", "LBN575", "LDN1262", "LBN534", "vdb158", "NGC7380", "NGC6543", "NGC2264", "NGC474", "NGC246", "NGC7479", "NGC7741", "IC5068", "SH2-155", "NGC7008", "NGC4676A", "NGC4536", "NGC2403", "IC11", "NGC2359", "IC5067", "NGC281", "IC44", "NGC6992", "NGC7293", "NGC6960", "IC4703", "NGC6618", "NGC6826", "NGC7662"]
#my_DSO_list = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30", "M31", "M32", "M33", "M34", "M35", "M36", "M37", "M38", "M39", "M40", "M41", "M42", "M43", "M44", "M45", "M46", "M47", "M48", "M49", "M50", "M51", "M52", "M53", "M54", "M55", "M56", "M57", "M58", "M59", "M60", "M61", "M62", "M63", "M64", "M65", "M66", "M67", "M68", "M69", "M70", "M71", "M72", "M73", "M74", "M75", "M76", "M77", "M78", "M79", "M80", "M81", "M82", "M83", "M84", "M85", "M86", "M87", "M88", "M89", "M90", "M91", "M92", "M93", "M94", "M95", "M96", "M97", "M98", "M99", "M100", "M101", "M102", "M103", "M104", "M105", "M106", "M107", "M108", "M109", "M110"]
#my_DSO_list = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
#my_DSO_list = ["M13", "M42", "M43", "M4", "M51", "M100", "M99", "M78", "M81", "M53"]

#my_DSO_list = ["M30"]

class DSO:

  def __init__(self, dso_name, today, tomorrow):
    self.the_object_name = str(dso_name).upper()
    self.theDate = today.strftime("%d.%m.%Y")
    self.theDate_american = today.strftime("%Y-%m-%d")
    self.today = today
    self.tomorrow = tomorrow

    if debug:
      print("Today: " + str(self.today))
      print("Tomorrow: " + str(self.tomorrow))

    self.civil_night_start, self.civil_night_end, self.nautical_night_start, self.nautical_night_end, self.astronomical_night_start, self.astronomical_night_end  = sky_utils.astro_night_times(self.theDate, latitude, longitude, debug)

    if debug:
      print("Latitude: " + str(latitude))
      print("Longitude: " + str(longitude))
      print("Nautical night start: " + str(self.nautical_night_start))
      print("Nautical night end: " + str(self.nautical_night_end))
      print("Astronomical night start: " + str(self.astronomical_night_start))
      print("Astronomical night end: " + str(self.astronomical_night_end))
    if self.astronomical_night_start == None and self.astronomical_night_end == None:
      self.astronomical_night_start = self.nautical_night_start
      self.astronomical_night_end = self.nautical_night_end
      if debug:
        print("Astronomical night start: " + str(self.astronomical_night_start))
        print("Astronomical night end: " + str(self.astronomical_night_end))

    ##############################################################################
    # `astropy.coordinates.SkyCoord.from_name` uses Simbad to resolve object
    # names and retrieve coordinates.
    #
    # Get the coordinates of the desired DSO:
    self.the_object = SkyCoord.from_name(self.the_object_name)
    if debug:
      print("SkyCoord: " + str(self.the_object))

    # http://vizier.u-strasbg.fr/cgi-bin/OType?$1
    result_table = ""
    try:
      # SELECT a.main_id, a.otype, b.B, b.V FROM basic AS a JOIN allfluxes AS b ON oidref = oid WHERE a.main_id='m13';
      #query = "SELECT main_id, otype FROM basic WHERE main_id IN ('" + str(self.the_object_name) + "')")
      query = "SELECT a.main_id, a.otype, b.B, b.V FROM basic AS a JOIN allfluxes AS b ON oidref = oid WHERE a.main_id='" + str(self.the_object_name) + "';"
      query = "SELECT a.main_id, a.otype, b.B, b.V, galdim_minaxis, galdim_majaxis FROM basic AS a JOIN allfluxes AS b ON b.oidref = oid JOIN ident AS c ON c.oidref = oid WHERE a.main_id='" + str(self.the_object_name) + "';"
      result_table = Simbad.query_tap(query)
    except Exception as e:
      print("Simbad lookup error for " + str(self.the_object_name) + ": " + str(e))
      #result_table = Simbad.query_tap("SELECT main_id, otype FROM basic WHERE main_id IN ('" + str(self.the_object_name) + "')")
      query = "SELECT a.main_id, a.otype, b.B, b.V FROM basic AS a JOIN allfluxes AS b ON oidref = oid WHERE a.main_id='" + str(self.the_object_name) + "';"
      query = "SELECT a.main_id, a.otype, b.B, b.V, galdim_minaxis, galdim_majaxis FROM basic AS a JOIN allfluxes AS b ON b.oidref = oid JOIN ident AS c ON c.oidref = oid WHERE a.main_id='" + str(self.the_object_name) + "';"
      result_table = Simbad.query_tap(query)
    if debug:
      print(result_table)
      print("Main id: " + str(result_table["main_id"]) + "; " + str(len(result_table["main_id"].pformat())))
    if len(result_table["main_id"].pformat()) == 2:
      if debug:
        print("DSO " + str(self.the_object_name) + " not found.")
      #sys.exit(0)
      self.object_type = "NONE"
    else:

      if debug:
        print("Query result lentgh: " + str(len(result_table["main_id"].pformat())))
        print(str(result_table["main_id"].pformat()))
        print(str(result_table["V"].pformat()))
        print(str(result_table["galdim_majaxis"].pformat()))

      if len(result_table["main_id"].pformat()) > 0:
        otype = result_table["otype"].pformat()[2].strip()
        if otype != "--":
          self.object_type = otype
        if debug:
          print("Main ID: " + str(result_table["main_id"].pformat()[0].strip())) #Main ID: main_id
          print("Main ID: " + str(result_table["main_id"].pformat()[1].strip())) #Main ID: -------
          print("Main ID: " + str(result_table["main_id"].pformat()[2].strip())) #Main ID: M   1
          '''
          main_id otype         B                 V         galdim_minaxis galdim_majaxis
                                                              arcmin         arcmin
          ------- ----- ----------------- ----------------- -------------- --------------
          M  31   AGN 4.360000133514404 3.440000057220459          70.79         199.53
          '''
          print("Brightness B: " + str(result_table["B"].pformat()[2].strip()) + " V: " + str(result_table["V"].pformat()[2].strip()))
          print("Size: " + str(result_table["galdim_majaxis"].pformat()[2].strip()) + " x " + str(result_table["galdim_minaxis"].pformat()[2].strip()))
          print("Object type: " + str(self.object_type))

        mag = result_table["V"].pformat()[2].strip()
        if mag != "--":
          self.magnitude = float(mag)
        else:
          self.magnitude = -1.0
        majax = result_table["galdim_majaxis"].pformat()[2].strip()  # arcmin
        if majax != "--":
          self.major_axis = float(majax)
        else:
          self.major_axis = -1.0
        minax = result_table["galdim_minaxis"].pformat()[2].strip()  # arcmin
        if minax != "--":
          self.minor_axis = float(minax)
        else:
          self.minor_axis = -1.0
      else:
        self.object_type = ""
        self.magnitude = -1.0
        self.major_axis = -1.0
        self.minor_axis = -1.0
        self.visible = False
        self.object_type_string = ""

    if self.object_type == "AGN":
      self.object_type_string = "Active galaxy nucleus"
    elif self.object_type == "SNR":
      self.object_type_string = "SuperNova remnant"
    elif self.object_type == "SFR":
      self.object_type_string = "Star forming region"
    elif self.object_type == "SFR":
      self.object_type_string = "Star forming region"
    elif self.object_type == "GNe":
      self.object_type_string = "Nebula"
    elif self.object_type == "RNe":
      self.object_type_string = "Reflection nebula"
    elif self.object_type == "GDNe":
      self.object_type_string = "Dark cloud (nebula)"
    elif self.object_type == "MoC":
      self.object_type_string = "Molecular cloud"
    elif self.object_type == "IG":
      self.object_type_string = "Interacting galaxies"
    elif self.object_type == "PaG":
      self.object_type_string = "Pair of galaxies"
    elif self.object_type == "GiP":
      self.object_type_string = "Galaxy in pair of galaxies"
    elif self.object_type == "CGG":
      self.object_type_string = "Compact group of galaxies"
    elif self.object_type == "CIG":
      self.object_type_string = "Cluster of galaxies"
    elif self.object_type == "BH":
      self.object_type_string = "Black hole"
    elif self.object_type == "LSB":
      self.object_type_string = "Low surface brightness galaxy"
    elif self.object_type == "SBG":
      self.object_type_string = "Starburst galaxy"
    elif self.object_type == "H2G":
      self.object_type_string = "HII galaxy"
    elif self.object_type == "GGG":
      self.object_type_string = "Galaxy"
    elif self.object_type == "Cl":
      self.object_type_string = "Cluster of stars"
    elif self.object_type == "GlC":
      self.object_type_string = "Globular cluster"
    elif self.object_type == "OpC":
      self.object_type_string = "Open cluster"
    elif self.object_type == "Cl*":
      self.object_type_string = "Open cluster"
    elif self.object_type == "LIN":
      self.object_type_string = "LINER-type active galaxy nucleus"
    elif self.object_type == "SyG":
      self.object_type_string = "Seyfert galaxy"
    elif self.object_type == "Sy1":
      self.object_type_string = "Seyfert 1 galaxy"
    elif self.object_type == "Sy2":
      self.object_type_string = "Seyfert 2 galaxy"
    elif self.object_type == "GiG":
      self.object_type_string = "Galaxy towards a group of galaxies"
    elif self.object_type == "As*":
      self.object_type_string = "Association of stars"
    elif self.object_type == "PN":
      self.object_type_string = "Planetary nebula"
    else:
      self.object_type_string = ""

    time = Time(str(self.theDate_american) + " 23:59:00") - utcoffset
    if debug:
      print("Observation time: " + str(time))

    ##############################################################################
    # `astropy.coordinates.EarthLocation.get_site_names` and
    # `~astropy.coordinates.EarthLocation.get_site_names` can be used to get
    # locations of major observatories.
    #
    # Use `astropy.coordinates` to find the Alt, Az coordinates of the DSO at as
    # observed from the current location today
    self.the_object_altaz = self.the_object.transform_to(AltAz(obstime=time, location=the_location))
    to_alt = self.the_object_altaz.alt
    to_az = self.the_object_altaz.az
    if debug:
      print(str(self.the_object_name) + "'s altitude = " + str(to_alt) + ", azimut = " + str(to_az))
    direction = sky_utils.compass_direction(to_az.value)
    if debug:
      print("Dir@: " + str(time) + ": " + str(direction))

    ##############################################################################
    # This is helpful since it turns out M33 is barely above the horizon at this
    # time. It's more informative to find M33's airmass over the course of
    # the night.
    #
    # Find the alt,az coordinates of the object at 100 times evenly spaced between 10pm
    # and 7am EDT:
    # +1: otherwise the dso graph does not match the x-axis ticks
    self.midnight = Time(str(self.theDate_american) + " 23:59:00") - utcoffset
    #self.delta_midnight = np.linspace(-2, 10, 100) * u.hour
    self.delta_midnight = np.linspace(-12, 12, 1000) * u.hour
    self.frame_night = AltAz(obstime=self.midnight + self.delta_midnight, location=the_location)
    self.the_objectaltazs_night = self.the_object.transform_to(self.frame_night)

    ##############################################################################
    # convert alt, az to airmass with `~astropy.coordinates.AltAz.secz` attribute:
    #the_objectairmasss_night = the_objectaltazs_night.secz
    ##############################################################################
    # Plot the airmass as a function of time:
    '''
      plt.plot(delta_midnight, the_objectairmasss_night)
      plt.xlim(-2, 10)
      plt.ylim(1, 4)
      plt.xlabel("Hours from EDT Midnight")
      plt.ylabel("Airmass [Sec(z)]")
      plt.show()
    '''

    ##############################################################################
    # Use  `~astropy.coordinates.get_sun` to find the location of the Sun at 1000
    # evenly spaced times between noon on July 12 and noon on July 13:
    from astropy.coordinates import get_sun
    self.delta_midnight = np.linspace(-12, 12, 1000) * u.hour
    self.times_overnight = self.midnight + self.delta_midnight
    self.frame_over_night = AltAz(obstime=self.times_overnight, location=the_location)
    self.sunaltazs_over_night = get_sun(self.times_overnight).transform_to(self.frame_over_night)


    ##############################################################################
    # Do the same with `~astropy.coordinates.get_body` to find when the moon is
    # up. Be aware that this will need to download a 10MB file from the internet
    # to get a precise location of the moon.
    from astropy.coordinates import get_body
    self.moon_over_night = get_body("moon", self.times_overnight)
    self.moonaltazs_over_night = self.moon_over_night.transform_to(self.frame_over_night)

    self.the_objectaltazs_over_night = self.the_object.transform_to(self.frame_over_night)
    self.visible = False
    self.max_alt, self.max_alt_direction, self.max_alt_az, self.max_alt_time, self.max_alt_during_night, self.max_alt_during_night_direction, self.max_alt_during_night_obstime, self.visible = self.max_altitudes(self.frame_over_night, self.the_objectaltazs_over_night)

    # moon data once it is available
    self.score_at_max_alt, self.top_score_at_max_alt, self.sub_text_moon_at_max_alt, self.moon_dir_at_max_alt, self.moon_alt_at_max_alt, self.moon_phase_percent_at_max_alt = self.moon_check_at_max_alt()

  def max_altitudes(self, frame_over_night, the_objectaltazs_over_night):
    try:
      if debug:
        print("Check object alt az during night time")
      dso_in_the_dark_ot = []
      dso_in_the_dark_alt = []
      dso_in_the_dark_az = []

      if debug:
        print("Astro night: " + str(self.astronomical_night_start) + "  " + str(self.astronomical_night_end))
        print("Nautical night: " + str(self.nautical_night_start) + "  " + str(self.nautical_night_start))
      for o in the_objectaltazs_over_night:
        dt = o.obstime.tt.datetime
        #if astronomical_night_start < dt < astronomical_night_end:
          #print(dt)
        if self.nautical_night_start < dt < self.nautical_night_end:
          #if debug:
          #  print("  " + str(o.obstime) + ": " + str(o.alt) + ", " + str(o.az))
          dso_in_the_dark_alt.append(o.alt.value)
          dso_in_the_dark_az.append(o.az.value)
          dso_in_the_dark_ot.append(o.obstime.tt.datetime)

      if debug:
        print(len(the_objectaltazs_over_night))
        print(len(dso_in_the_dark_alt))

      if len(dso_in_the_dark_alt)>0:
        dso_in_the_dark_alt_max = max(dso_in_the_dark_alt)
        index_alt_max = dso_in_the_dark_alt.index(max(dso_in_the_dark_alt)) #np.argmax(dso_in_the_dark_alt)
        if debug:
          print("max: " + str(dso_in_the_dark_alt_max) + " at " + str(dso_in_the_dark_ot[index_alt_max]))

        # check whether object is visible during the night
        visible = False
        if len(dso_in_the_dark_alt)>0:
          v = []
          for a in dso_in_the_dark_alt:
            if a > 5:
              v.append(1)
          if debug:
            print(len(dso_in_the_dark_alt))
            print(len(v))
          if len(v) > 30:
            visible = True # DSO is visible for at least 30 minutes during the night time
          else:
            visible = False

        if debug:
          print("DSO night max alt: " + str(dso_in_the_dark_alt_max) + " at " + str(dso_in_the_dark_ot[index_alt_max]))
        dso_in_the_dark_alt_max_az = dso_in_the_dark_az[index_alt_max]
        direction_max_alt = sky_utils.compass_direction(dso_in_the_dark_alt_max_az)
        if debug:
          print("DSO night max alt direction: " + str(direction_max_alt))

        # Direction of total max. altitude
        alt_max_total = max(the_objectaltazs_over_night.alt.value)
        index_alt_max_total = np.argmax(the_objectaltazs_over_night.alt)
        direction_max_alt_total = sky_utils.compass_direction(the_objectaltazs_over_night.az[index_alt_max_total].value)

        alt_max_total_obstime = dso_in_the_dark_ot[index_alt_max] #frame_over_night.obstime[index_alt_max_total]
        max_alt_txt = "Max. Alt. " + str(round(alt_max_total,2)) + "deg at: " + str(alt_max_total_obstime) + " in " + str(direction_max_alt_total)
        if debug:
          print(max_alt_txt)
      else:
        return -1, -1, -1, -1, -1, -1, False
      return dso_in_the_dark_alt_max, direction_max_alt, dso_in_the_dark_alt_max_az, dso_in_the_dark_ot[index_alt_max], alt_max_total, direction_max_alt_total, alt_max_total_obstime, visible
    except Exception as e:
      print(str(e))


  def moon_check_at_max_alt(self):
    score = False
    top_score = False
    sub_text = "    "

    try:
      moon_rise, moon_set, full_moon, moon_phase, moon_phase_percent, moon_alt, moon_az, moon_dist = sky_utils.moon_data(self.theDate, self.max_alt_time.strftime("%H:%M"))
      moon_dir = sky_utils.compass_direction(moon_az)
      if debug:
        print("  Moon rise: " + str(moon_rise) + " set: " + str(moon_set) + " next full moon: " + str(full_moon) + " phase: " + str(moon_phase) + " (" + str(moon_phase_percent) + " %)")
        print("  Moon alt " + str(moon_alt) + " az " + str(moon_az) + " dir " + str(moon_dir))

      if float(moon_alt) < 0:
        msg = "TOP: Moon is below the horizon at " + str(self.max_alt_time.strftime("%d.%m.%Y %H:%M"))
        if debug:
          print(msg)
        score = True
        top_score = True
        sub_text += "\n    " + msg
      if moon_dir != self.max_alt_direction:
        msg = "Quite good: Moon dir: " + str(moon_dir) + " (" + str(round(moon_az,0)) + ") " + ", DSO dir: " + str(self.max_alt_direction) + " (" + str(round(self.max_alt_az,0)) + ")"
        if debug:
          print(msg)
        score = True
        sub_text += "\n    " + msg
      if moon_phase_percent < 50:
        msg = "Quite nice: Moon illumination is below 50 %: " + str(moon_phase_percent) + " %"
        if debug:
          print(msg)
        score = True
        sub_text += "\n    " + msg
      return score, top_score, sub_text, moon_dir, moon_alt, moon_phase_percent
    except Exception as e:
      print("Moon check error: " + str(e))

def plot(dsolist):
  try:
    plt.clf()
    plt.cla()
    plt.close()

    plt.figure(facecolor='lightgrey')
    plt.style.use(astropy_mpl_style)

    quantity_support()

    sub_text = ""

    for dso in dsolist:
      #direction_20, direction_22, direction_0, direction_2, direction_4, direction_6 = dso.observation_night_directions()

      score = False
      top_score = False

      dso_max_alt = round(max(dso.the_objectaltazs_over_night.alt.value),0)
      index_alt_max_total = np.argmax(dso.the_objectaltazs_over_night.alt)
      az = dso.the_objectaltazs_over_night.az[index_alt_max_total].value
      direction_max_alt_total = sky_utils.compass_direction(az)
      if debug:
        print("  max alt: " + str(dso_max_alt) + " at " + str(dso.max_alt_time.strftime("%H:%M")) + " in " + str(direction_max_alt_total) + " (" + str(round(az,0)) + ")")

      dt = dso.max_alt_time
      if dso.astronomical_night_start < dt < dso.astronomical_night_end:
        if debug:
          print("##### OK in " + str(dso.max_alt_time.strftime("%m")) + " #####")
          print("DSO " + str(dso.the_object_name) + " appears during the astronomical night. Max. alt " + str(dso_max_alt) + " is reached at " + str(dso.max_alt_time.strftime("%H:%M")))
          print("Astronomical night: " + str(dso.astronomical_night_start.strftime("%H:%M")) + " - " + str(dso.astronomical_night_end.strftime("%H:%M")))
        sub_text += "\n\n" + str(dso.the_object_name) + " max. altitude " + str(dso_max_alt) + " is reached at " + str(dso.max_alt_time.strftime("%d.%m.%Y %H:%M")) + " in " + str(direction_max_alt_total) + " (" + str(round(az,0)) + ")"

        # consider moon phase/illumination/position
        #score, top_score, sub_text_moon = moon_check(dso, direction_max_alt_total)
      sub_text += dso.sub_text_moon_at_max_alt

      ##############################################################################
      # Make a beautiful figure illustrating nighttime and the altitudes of the DSO and
      # the Sun over that time:
      if debug:
        print("Plot " + str(dso.theDate))

      # use solid colours for good times, pastel colors for inappropriate times

      #https://htmlcolorcodes.com/color-names/
      # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
      if ".01." in dso.theDate:
        color_code = "#C0C0C0" # silver
        if dso.score_at_max_alt:
          color_code = "#708090" # SlateGray
      elif ".02." in dso.theDate:
        color_code = "#F0F8FF" # aliceblue
        if dso.score_at_max_alt:
          color_code = "#00BFFF" # DeepSkyBlue
      elif ".03." in dso.theDate:
        color_code = "#FAEBD7" # linen
        if dso.score_at_max_alt:
          color_code = "#D2691E" # Chocolate
      elif ".04." in dso.theDate:
        color_code = "#FFEBCD" # blanchedalmond
        if dso.score_at_max_alt:
          color_code = "#A0522D" # Sienna
      elif ".05." in dso.theDate:
        color_code = "#87CEFA" # lightskyblue
        if dso.score_at_max_alt:
          color_code = "#4169E1" # RoyalBlue
      elif ".06." in dso.theDate:
        color_code = "#AFEEEE" # PaleTurquoise
        if dso.score_at_max_alt:
          color_code = "#00CED1" # DarkTurquoise
      elif ".07." in dso.theDate:
        color_code = "#98FB98" # PaleGreen
        if dso.score_at_max_alt:
          color_code = "#3CB371" # MediumSeaGreen
      elif ".08." in dso.theDate:
        color_code = "#FFA07A" # LightSalmon
        if dso.score_at_max_alt:
          color_code = "#FFA500" # orange
      elif ".09." in dso.theDate:
        color_code = "#CD5C5C" # indianred
        if dso.score_at_max_alt:
          color_code = "#DC143C" # crimson
      elif ".10." in dso.theDate:
        color_code = "#D8BFD8" # Thistle
        if dso.score_at_max_alt:
          color_code = "#9932CC" # darkorchid
      elif ".11." in dso.theDate:
        color_code = "#7B68EE" # mediumslateblue
        if dso.score_at_max_alt:
          color_code = "#191970" # MidnightBlue
      elif ".12." in dso.theDate:
        color_code = "#E6E6FA" # Lavender
        if dso.score_at_max_alt:
          color_code = "#4B0082" # indigo
      else:
        color_code = "#FFFACD" # LemonChiffon
        if dso.score_at_max_alt:
          color_code = "#9ACD32" # yellowgreen

      label_text = str(dso.max_alt_time.strftime("%d.%m"))
      if dso.top_score_at_max_alt:
        label_text = str(dso.max_alt_time.strftime("%d.%m")) + " " +  str(dso.max_alt_time.strftime("%H:%M"))
      alpha_value = 1
      if not dso.top_score_at_max_alt:
        alpha_value = 0.3
      plt.scatter(
          dso.delta_midnight,
          dso.the_objectaltazs_over_night.alt,
          #c=dso.the_objectaltazs_over_night.az.value,
          c=color_code,
          label=label_text,
          linewidths=0,
          s=8,
          alpha=alpha_value)
      #if len(sub_text)>0:
      #  plt.figtext(0.1,-0.5, sub_text, ha="center", va="baseline", fontsize=10, bbox={"facecolor":"lightyellow", "alpha":0.5, "pad":5})
      #  #plt.text(0.5,0.5, sub_text, fontsize=10)
    print(sub_text)

    '''
    plt.fill_between(
        dso.delta_midnight,
        0 * u.deg,
        90 * u.deg,
        dso.sunaltazs_over_night.alt < 7 * u.deg,
        color="0.55",
        zorder=0,)  # twilight time
    plt.fill_between(
        dso.delta_midnight,
        0 * u.deg,
        90 * u.deg,
        dso.sunaltazs_over_night.alt < -13 * u.deg,
        color="0.35",
        zorder=0,)  # night time
    plt.fill_between(
        dso.delta_midnight,
        0 * u.deg,
        90 * u.deg,
        dso.sunaltazs_over_night.alt < -19 * u.deg,
        color="k",
        zorder=0,)
    '''

    the_year_format = dso.today.strftime("%Y")
    plt.title(str(dso.the_object_name) + " " + str(the_year_format)) # + ": " + str(direction_20) + "-" + str(direction_22) + "-" + str(direction_0) + "-" + str(direction_2) + "-" + str(direction_4) + "-" + str(direction_6))
    plt.colorbar().set_label("Azimuth [deg]")
    plt.legend(loc="upper center", fontsize="small", ncol=3)
    # x-axis labels
    xt = (np.arange(13) * 2 - 12)
    plt.xlim(-12 * u.hour, 12 * u.hour)
    plt.xticks(xt * u.hour)
    for i in range(len(xt)):
      if xt[i]+24 < 24:
        xt[i] = xt[i]+24
      else:
        xt[i] = xt[i]
    labels = [item.get_text() for item in plt.gca().get_xticklabels()]
    for i in range(len(labels)):
      labels[i] = xt[i]
    # replace x-axis labels by actual hours
    plt.gca().set_xticklabels(labels)

    plt.ylim(0 * u.deg, 90 * u.deg)
    plt.xlabel("Hours from Midnight") # EDT: Eastern Daylight Time
    plt.ylabel("Altitude [deg]")

    plot_name = base_dir + "DSO_" + str(dso.the_object_name) + "_" + str(the_year_format) + ".png"
    if platform.system() == "Linux":
      if os.path.isdir(base_dir):
        plot_name = base_dir + "DSO_" + str(dso.the_object_name) + "_" + str(the_year_format) + ".png"
    if plot_name != "":
      plt.savefig(plot_name)
      if debug:
        print("Saved: " + str(plot_name))
    else:
      print("Plot name missing on " + str(platform.system()) + " . Nothing saved.")
    #plt.show()
  except Exception as e:
    print("DSO observation night plotting error " + str(dso.the_object_name) + ": " + str(e))

def is_summertime(dt, timeZone):
   aware_dt = timeZone.localize(dt)
   return aware_dt.dst() != datetime.timedelta(0,0)

def sort_DSOs(dso_list):
  # sort by max. altitude time
  dsol = sorted(dso_list, key=lambda x: x.max_alt_time)
  if debug:
    print("\n\n\n")
    print("Sorted by max. altitude time:")

  astronomical_night_start, astronomical_night_end = "",""
  nautical_night_start, nautical_night_end = "", ""
  astronomical_night_dsos = []
  nautical_night_dsos = []
  invisible_dsos = []
  for dso in dsol:
    dt = dso.max_alt_time
    astronomical_night_start = dso.astronomical_night_start
    astronomical_night_end = dso.astronomical_night_end
    nautical_night_start = dso.nautical_night_start
    nautical_night_end = dso.nautical_night_end

    if options.moon:
      if debug:
        print("###" + str(dso.score_at_max_alt) + ", " + str(dso.top_score_at_max_alt) + ", " + str(dso.sub_text_moon_at_max_alt))

    if dso.max_alt > 0:
      if dso.astronomical_night_start < dt < dso.astronomical_night_end:
        #dso_max_alt = round(max(dso.the_objectaltazs_over_night.alt.value),0)
        #index_alt_max_total = np.argmax(dso.the_objectaltazs_over_night.alt)
        #az = dso.the_objectaltazs_over_night.az[index_alt_max_total].value
        #direction_max_alt_total = sky_utils.compass_direction(az)
        if debug:
          print(dso.the_object_name + ": " + str(dso.max_alt) + " in " + str(dso.max_alt_direction) + " at " + str(dso.max_alt_time) + " (astronomical night)")
        if options.moon:
          if options.justthetopones:
            if "TOP" in dso.sub_text_moon_at_max_alt:
              if options.direction != None:
                if str(options.direction) in str(dso.max_alt_direction):
                  astronomical_night_dsos.append(dso)
              else:
                astronomical_night_dsos.append(dso)
          else:
            if "TOP" in dso.sub_text_moon_at_max_alt or "Quite" in dso.sub_text_moon_at_max_alt:
              if options.direction != None:
                if str(options.direction) in str(dso.max_alt_direction):
                  astronomical_night_dsos.append(dso)
              else:
                astronomical_night_dsos.append(dso)
        else:
          if options.direction != None:
            if str(options.direction) in str(dso.max_alt_direction):
              astronomical_night_dsos.append(dso)
          else:
            astronomical_night_dsos.append(dso)
      elif dso.nautical_night_start < dt < dso.nautical_night_end:
        if debug:
          print(dso.the_object_name + ": " + str(dso.max_alt) + " in " + str(dso.max_alt_direction) + " at " + str(dso.max_alt_time) + " (nautical night)")
        if options.moon:
          if options.justthetopones:
            if "TOP" in dso.sub_text_moon_at_max_alt:
              if options.direction != None :
                if str(options.direction) in str(dso.max_alt_direction):
                  nautical_night_dsos.append(dso)
              else:
                nautical_night_dsos.append(dso)
          else:
            if "TOP" in dso.sub_text_moon_at_max_alt or "Quite" in dso.sub_text_moon_at_max_alt:
              if options.direction != None:
                if str(options.direction) in str(dso.max_alt_direction):
                  nautical_night_dsos.append(dso)
              else:
                nautical_night_dsos.append(dso)
        else:
          if options.direction != None:
            if str(options.direction) in str(dso.max_alt_direction):
              nautical_night_dsos.append(dso)
          else:
            nautical_night_dsos.append(dso)
    else:
      invisible_dsos.append(dso)

  if debug:
    print("Astronomical night: " + str(astronomical_night_start) + " - " + str(astronomical_night_end))
    print("Nautical night: " + str(nautical_night_start) + " - " + str(nautical_night_end))
  return astronomical_night_start, astronomical_night_end, astronomical_night_dsos, nautical_night_start, nautical_night_end, nautical_night_dsos, invisible_dsos

if __name__ == '__main__':

  try:
    ######################################################################################
    # Use `astropy.coordinates.EarthLocation` to provide the location of the desired time
    the_location = EarthLocation(lat=latitude, lon=longitude, height=elevation)
    now = datetime.datetime.now()
    just_now = now.strftime("%Y-%m-%d %H:%M:%S")
    theDate = now.strftime("%d.%m.%Y")
    theYear = now.strftime("%Y")
    theDate_today = now.strftime("%Y-%m-%d")

    timeZone = pytz.timezone(config.coordinates["timezone"])
    if is_summertime(now, timeZone):
      utcoffset = +2 * u.hour  # +2 summertime, +1 wintertime
      if debug:
        print("Summertime: UTC+2")
    else:
      utcoffset = +1 * u.hour
      if debug:
        print("Wintertime: UTC+1")

    tomorrow = today + datetime.timedelta(days=1)
    if debug:
      print("Now: " + str(now))
      print("The day: " + str(today))
      print("The day after: " + str(tomorrow))

    if options.best:
      if options.dso:
        # single DSO
        dso_list = []
        # loop over 12 dates/year
        for the_month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
          the_date = "01." + str(the_month) + "." + str(theYear)
          if debug:
            print("Calculate visibility of " + str(dso_name) + " at " + str(the_date))
          the_day = today.replace(day=int(1), month=int(the_month), year=int(theYear))
          the_tomorrow = the_day + datetime.timedelta(days=1)
          dso = DSO(dso_name, the_day, the_tomorrow)
          dso_list.append(dso)
        plot(dso_list)
      else:
        # loop over all DSOs
        for dso_name in my_DSO_list:
          dso_list = []
          # loop over 12 dates/year
          for the_month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            the_date = "01." + str(the_month) + "." + str(theYear)
            if debug:
              print("Calculate visibility of " + str(dso_name) + " at " + str(the_date))
            the_day = today.replace(day=int(1), month=int(the_month), year=int(theYear))
            the_tomorrow = the_day + datetime.timedelta(days=1)
            dso = DSO(dso_name, the_day, the_tomorrow)
            dso_list.append(dso)
          #print(dso_list)
          plot(dso_list)

    elif options.tonight:
      print("Find best DSOs for tonight, ordered by their max. altitude...")
      dso_list = []
      for dso_name in my_DSO_list:
        dso = DSO(dso_name, today, tomorrow)
        dso_list.append(dso)

      result_msg = " Best DSOs for " + str(today.strftime("%d.%m.") + " - " + str(tomorrow.strftime("%d.%m.%Y")))

      astronomical_night_start, astronomical_night_end, astronomical_night_dsos, nautical_night_start, nautical_night_end, nautical_night_dsos, invisible_dsos = sort_DSOs(dso_list)

      msg = "\n\nNautical night: " + str(nautical_night_start.strftime("%d.%m.%Y %H:%M")) + " - " + str(nautical_night_end.strftime("%d.%m.%Y %H:%M"))
      print(len(nautical_night_dsos))
      print(msg)
      result_msg += msg
      for ndso in nautical_night_dsos:
        msg = "  " + ndso.the_object_name + ": " + str(round(ndso.max_alt,0)) + " in " + str(ndso.max_alt_direction) + " at " + str(ndso.max_alt_time.strftime("%H:%M")) # + " (nautical night)")
        if options.moon:
          msg += "\n" + str(ndso.sub_text_moon_at_max_alt)
        print(msg)
        result_msg += msg

      msg = "\n\nAstronomical night: " + str(astronomical_night_start.strftime("%d.%m.%Y %H:%M")) + " - " + str(astronomical_night_end.strftime("%d.%m.%Y %H:%M"))
      print(len(astronomical_night_dsos))
      print(msg)
      result_msg += msg
      for asdso in astronomical_night_dsos:
        msg = "  " + asdso.the_object_name + ": " + str(round(asdso.max_alt,0)) + " in " + str(asdso.max_alt_direction) + " at " + str(asdso.max_alt_time.strftime("%H:%M")) # + " (astronomical night)")
        if options.moon:
          msg += "\n" + str(asdso.sub_text_moon_at_max_alt)
        print(msg)
        result_msg += msg

      if len(invisible_dsos)>0:
        msg = "\n\nInvisible DSOs:"
        print(msg)
        result_msg += msg
        for idso in invisible_dsos:
          msg = "  " + idso.the_object_name + ": " + str(round(idso.max_alt,0)) + " in " + str(idso.max_alt_direction) + " at " + str(idso.max_alt_time.strftime("%H:%M"))
        print(msg)
        result_msg += msg

  except Exception as e:
    print("DSO observation planning error " + str(dso_name) + ": " + str(e))
  sys.exit(0)
