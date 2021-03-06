Configuration
=============

KCS uses a configuration file that sets most of the default
settings. The configuration file is in TOML format, as an attempt to
find a middle ground between more complicated (e.g. YAML) and very
simple (INI) formats.

Note that this configuration provides the default settings; these
would usually be constants in a Python script. Often, instead of
providing a configuration file, it is clearer (and easier) to supply
extra or changed options on the command line (as in the :ref:`usage
guide <usage-guide>`), or as arguments to a function call (as in the
:ref:`example Python script <example-script>`).

The default configuration file is, in fact, a long Python string, and
can be found in ``kcs.config.default`` as ``CONFIG_TOML_STRING``. You
should, however, rarely need to access it directly. Instead, use the
``kcs.config.default_config`` object, which is a Python (nested)
dictionary that maps directly to this TOML string.

If you only use the command line runnable modules, you can obtain the
TOML configuration file by executing

.. code-block:: bash

    python -m kcs.config > my-config.toml

This will dump the configuration file into the ``my-config.toml``
file, which can be edited to your liking, and then used with other
commands using the ``-C`` or ``--config`` option, e.g.

.. code-block:: bash

    python -m    python -m kcs.tas_change  @cmip-tas-global-averaged.list \
        --outfile=tas_change_cmip.csv --config my-config.toml

The default configuration file is commented in various places, and is
also listed at the end of this section. (The comments are the reason
the default configuration is in the form of a string: keeping it as a
Python object would lose the comments once transformed into a TOML
string or file.)

Note that in TOML, some string rules apply to values: strings should
always be quoted (with double quote characters). It is possible to
have multiline strings, with triple (double) quotes, similar to
Python. Floating point values should always contain a fractional part
or exponent (or both); otherwise, the value is interpreted as an
integer, or invalid. This should be clear from the default
configuration file, where, for example, the percentiles are all
floating points, even though the default percentiles happen to be all
integer values. For more details, see the `TOML specification
<https://github.com/toml-lang/toml>`_.


The configuration file is made up of several sections; these
correspond one-to-one to the main keys in the ``default_config``
object. These sections can be in random order, and are:

* scenario

  Definitions belonging to the requrested scenarios, such as the
  names, epochs, percentiles to match with the annual and percentage
  of precipitation change.

* areas

  Definitions of the possible areas of concern. For rectangles, use
  ``w``, ``e``, ``s`` and ``n`` indicators, though it is also possible
  to use ``lat`` and ``lon`` with a 2-element array of values. For
  single points, use just ``lat`` and ``lon`` with a single
  value. Note that all these values should be floating point
  values. For a global area, there is a special string value
  ``"global"``.

* variables

  Some definitions about variables. Currently, it only sets a list of
  short variable names for which relative changes should be
  calculated, such as ``pr``.

* statistics

  Which statistics (mean, percentiles) to calculate. There are two
  subsections, one for the change in temperature (``tas_change``),
  which leads to the calculation of the steering table; and the
  statistics for the local, regional, changes in e.g. precipitation
  and temperature. (Note: this is not yet fully implemented, end of
  March 2020.)

* resampling

  This sets the most important parameters for the three resampling
  steps. The conditions for resampling step 2 are given through
  another file, as this would be a lengthy section in itself. An
  example of this file can be found in the ``config/``
  directory. There is not yet a completely built-in configuration for
  this file, that is, at least the default should be copied into the
  current working directory (it will then automatically be found and
  read).

* data

  This section is a long one, with various definitions about the input
  data sets. It is split into a few sections: one about cmip data, one
  about "extra" data (concerning the model of interest), and one for
  matching datasets (i.e., historical and future experiments). The
  latter has subsections in the cmip and extra subsections, which can
  override the base "data.matching" settings. There is also a
  "data.filenames" section, which defines the filename format for
  various dataset through a regular expression pattern. This is needed
  when attributes are deduced from the filenames (e.g., if the
  attributes are not available directly through a data file).

* plotting

  This section is defined, but its functionality is, as of end of
  March 2020, not yet implemented. Once implemented, this allows one
  to control e.g. the figure size, colors, transparency (alpha) and a
  few other options.


If you want to make changes, use the outputted configuration file,
edit it, then supply it on the command line or read it explicitly with
``kcs.config.read_config("my-config.toml")`` (for use of the latter,
see the :ref:`example-script`).

It is possible to only output a single section from the default
configuration, edit that, and supply that as configuration file. This
shortens the local (user) configuration file considerably, and may
make it clearer what has been changed. Supply the section name after
the ``kcs.config`` module to output just that section, for example:

.. code-block:: bash

    python -m kcs.config resample > resample-config.toml

Note that configuration files should always have complete sections:
there is no guarantee (at least, not yet) that missing key-value
settings will be taken from the built-in configuration. While this can
make it less clear what changes have been made in the user
configuration file, it keeps the configuration for each section nicely
together.


Default user configuration
--------------------------

It is possible to have a default user configuration file in the
current working directory, that is automatically read by scripts
(runnable modules). That is, therer is no need to supply the
``--config <my-config-file.toml>`` option.

This has an advantage and disadvantage: the advantage is cleaner
scripts, that are not befuddled with options that can confuse a
reader. The disadvantage is that if such a default user configuration
exists in one place, but not in another place (either another working
directory, or on the machine of a completely other user), the
configuration and thus the results, may be quite different. If you use
this feature, always make sure this configuration is supplied when
publishing the results (even if just emailing the results to a
colleague).

This default user configuration file should be called
``kcs-config.toml`` and be located in the current working
directory. For the (disadvantage) reason stated above, it is not a
hidden file, nor is it located user-wide in, for example, the user's
home directory or an XDG configuration directory.

The ``kcs-config.toml`` file is *not* automatically read when using a
Python script; it only works with command line scripts, as in the
:ref:`usage guide <usage-guide>`. When using a Python script, you can
still read this file either explicitly with
``kcs.config.read_config("kcs-config.toml")``, or implicitly with
``kcs.config.read_config()``. The latter will attempt to read the
default user configuration file, and if not found, revert back to the
built-in configuration.


Full annotated configuration
----------------------------

(Valid end of March 2020)

Below is the full configuration listed, with comments annotating
various parts. This is the same that one would get from running
``python -m kcs.config``, and, in fact, the same as
``kcs.config.default.CONFIG_TOML_STRING``.

.. code-block:: toml

    # Notes about values in the TOML config file:
    # - strings should always be quoted. Multi-line strings are possible
    #   using triple-quotes, but should not be necessary in this config file
    # - floating point values require a decimal dot, or an exponent (or
    #   both). Otherwise, they are interpreted as integers.
    # More information about the TOML config format: https://github.com/toml-lang/toml



    [scenario]

    [scenario.defs]
    # Note: extra definitions for a name or precip do not have to be commented out below, even if the corresponding
    # scenarios are commented-out above

    # percentile of CMIP tas for a given epoch that the 'W' and 'G' scenarios correspond to
    W = 90.0
    G = 10.0
    # percent change in precipitation (times global tas increase) for 'L' and 'H' scenarios
    L = 4.0
    H = 8.0


    # Scenarios to use.
    # This defines only the names and epoch.
    # Values (what G/W and L/H correspond to) are filled in below.
    # Comment-out scenarios of no-interest.
    [scenario.G_L2050]
    name = "G"
    epoch = 2050
    precip = "L"
    [scenario.W_L2050]
    name = "W"
    epoch = 2050
    precip = "L"
    [scenario.G_H2050]
    name = "G"
    epoch = 2050
    precip = "H"
    [scenario.W_H2050]
    name = "W"
    epoch = 2050
    precip = "H"
    [scenario.G_L2085]
    name = "G"
    epoch = 2085
    precip = "L"
    [scenario.W_L2085]
    name = "W"
    epoch = 2085
    precip = "L"
    [scenario.G_H2085]
    name = "G"
    epoch = 2085
    precip = "H"
    [scenario.W_H2085]
    name = "W"
    epoch = 2085
    precip = "H"


    [areas]
    # Define areas of interest
    # Use w, e, s, n identifiers in a inline-table/map/dict for a rectangular area
    # Or lat, lon in a inline-table/map/dict for a single point
    # Or the special value "global"
    # Values for w/e/s/n/lat/lon should all be floating point.
    # Shapefiles and masks are not yet supported.
    global = "global"
    nlpoint = {lat = 51.25, lon = 6.25}
    nlbox = {w = 4.5, e = 8.0, s = 50.5, n = 53.0}
    weurbox = {w = 4.0, e = 14.0, s= 47.0, n = 53.0}
    rhinebasin = {w = 6.0, e = 9.0, n = 52.0, s = 47.0}

    [variables]
    # Some generic configuration regarding variables

    # For which variables to calculate a relative change,
    # instead of an absolute change (compare 'pr' versus 'tas')
    # A list of short variable names.
    relative = ["pr"]


    [data]
    # Some generic configuration for the input data
    # This assumes NetCDF files with proper (CF-conventions) attributes

    [data.attributes]
    # Define the attribute names for meta information.
    # Each definition should be a list: this allows to handle different
    # conventions (e.g., between CMIP5 and CMIP6) if one is not available.
    experiment = ["experiment_id"]
    model = ["model_id", "source_id"]
    realization = ["realization", "realization_index"]
    initialization = ["initialization_method", "initialization_index"]
    physics = ["physics_version", "physics_index"]
    prip = ["parent_experiment_rip", "parent_variant_label"]
    var =  ["variable_id"]

    # What is the attribute value that indicates historical experiments?
    # Everything else is assumed to be a future experiment.
    # This value is case-insensitive.
    historical_experiment = "historical"

    [data.extraction]
    template = "data/{var}-{area}-averaged/{filename}.nc"


    [data.filenames]
    # Definitions of filename patterns, to obtain attribute information from.
    # Several are given, for various conventions.
    # All are tried, until a match is found.

    # Regexes can be notably hard to read, especially in this case, since every
    # blackslash needs to be escaped, resulting in lots of double backslashes.

    [data.filenames.esmvaltool]
    pattern = """^CMIP\\d_\
    (?P<model>[-A-Za-z0-9]+)_\
    (?P<mip>[A-Za-z]+)_\
    (?P<experiment>[A-Za-z0-9]+)_\
    r(?P<realization>\\d+)\
    i(?P<initialization>\\d+)\
    p(?P<physics>\\d+)_\
    (?P<var>[a-z]+)_\
    .*\\.nc$\
    """

    [data.filenames.cmip5]
    pattern = """^\
    (?P<var>[a-z]+)_\
    (?P<mip>[A-Za-z]+)_\
    (?P<model>[-A-Za-z0-9]+)_\
    (?P<experiment>[A-Za-z0-9]+)_\
    r(?P<realization>\\d+)\
    i(?P<initialization>\\d+)\
    p(?P<physics>\\d+)_\
    .*\\.nc$\
    """

    [data.filenames.cmip6]
    pattern = """^\
    (?P<var>[a-z]+)_\
    (?P<mip>[A-Za-z]+)_\
    (?P<model>[-A-Za-z0-9]+)_\
    (?P<experiment>[A-Za-z0-9]+)_\
    r(?P<realization>\\d+)\
    i(?P<initialization>\\d+)\
    p(?P<physics>\\d+)\
    f\\d+_\
    gn_\
    .*\\.nc$\
    """

    [data.filenames.ecearth]
    pattern = """^\
    (?P<var>[a-z]+)_\
    (?P<mip>[A-Za-z]+)_\
    (?P<model>[-A-Za-z0-9]+)_\
    (?P<experiment>[A-Za-z0-9]+)_\
    .*\\.nc$\
    """


    [data.cmip]
    # Configuration for everything that considers CMIP data


    # Actual timespan a given scenario epoch corresponds to
    periods = {2050 = [2036, 2065], 2085 = [2071, 2100]}

    # Control period defines the reference period to which to compare (and
    # possibly normalize) to.
    # CMIP5 would be [1980, 2009], CMIP6 would be [1990, 2019]
    control_period = [1990, 2019]

    # Normalize the CMIP data to the control period.
    # Choices are "model", "experiment" or "run". These options vary from
    # the most to the least spread of normalized data around the control period.
    # Leave blank to not normalize (usually a bad idea).
    norm_by = "run"

    # Calculate the tas change for a specific seasonal average, or a yearly average
    # Choices are "year", "djf", "mam", "jja", "son".
    season = "year"


    [data.matching]
    # Configuration how to match and concatenate CMIP historical and future experiments

    # Match future and historical runs by model (very generic) or ensemble (very specific).
    by = "ensemble"

    # Where to get the match info from. Either (NetCDF) 'attributes' or the 'filename' pattern
    # Should always be a list: the later options in the list serve as a fallback in case earlier
    # options don't succeed
    info_from = ["attributes", "filename"]

    # What to do when a future ensemble can't be matched:
    # - "error": raise an error, and stop the program
    # - "remove": remove (ignore) the future ensemble
    # - "randomrun": pick a random historical run that matches all attributes, except the realization
    # - "random": pick a random historical run from all ensembles of that model
    on_fail = "randomrun"

    [data.cmip.matching]
    # Empty: all values are taken from [data.matching]


    [data.extra]
    # Configuration for additional data
    # This is the data of interest, for which a steering table will be
    # calculated, and whose runs will be resampled.

    control_period = [1990, 2019]

    [data.extra.matching]
    # An empty string means the datasets are already concatenated datasets: historical + future.
    by = ""

    # Any other key not defined here (match_info_from, on_no_match) are taken from [data.matching]



    [statistics]
    # Which statistics (mean and percentiles) to calculate.
    # There are two subsets:
    # 1. the statistics for the tas change (which leads to the steering table)
    # 2. the statistics for the seasonal-regional change plots

    [statistics.tas_change]
    # A list of floating point numbers (matching between these floating
    # point numbers for finding the right percentiles, is done with an
    # accuracy of 0.0001 tolerance).
    percentiles = [5.0, 10.0, 25.0, 50.0, 75.0, 90.0, 95.0]
    # Calculate the mean as well
    mean = true

    [statistics.regional_changes]
    percentiles = [5.0, 10.0, 25.0, 50.0, 75.0, 90.0, 95.0]
    mean = true


    [plotting]
    figsize = [8.0, 8.0]

    [plotting.tas_increase]
    # Configuration for global temperature increase plot

    # CMIP percentiles levels to plot
    # Each level needs a name, to be re-used in the styline configuration
    levels = {extreme = [5.0, 95.0], middle = [10.0, 90.0], narrow = [25.0, 75.0]}

    # Smooth the plot across time; value should be an integer. Leave blank for no smoothing.
    rolling_window = 10

    [plotting.tas_increase.extra_data]
    # Overplot extra datasets?
    overplot = true
    # Plot averaged data, or individual runs
    average_data = true
    # Smooth with rolling window; same as for CMIP data
    rolling_window = 10


    [plotting.tas_increase.labels]
    x = "Year"
    y = "Increase [${}^{\\circ}$]"

    [plotting.tas_increase.range]
    # Use a 2-element list. Leave blank to let Matplotlib figure things out.
    x = [1950, 2100]  # years, in integers
    y = [-1.0, 6.0]   # always float

    [plotting.tas_increase.styles]
    # Re-use the level names above.
    # Use Matplotlib color and alpha codes.
    # Anything not given is 'black' (color) and 1.0 (alpha; opaque).
    colors = {extreme = "#bbbbbb", middle = "#888888", narrow = "#555555", extra_data = "#669955"}
    alpha = {extreme = 0.8, middle = 0.4, narrow = 0.2}



    [resampling]

    nsections = 6
    nstep1 = 1000
    nstep3 = 8
    # Monte-Carlo number of samples
    nsample = 10_000

    # Number of simultaneous processes for the calculations of step 1.
    # Note that for relatively few input runs (< 12), the overhead
    # generally costs more than multiprocessing wins.
    nproc = 1

    # TOML file that defines the percentiles ranges used in step 2
    step2_conditions = "step2.toml"


    # Penalties for number of (multiple) occurrences of segment in resamples, in step 3.
    # Starts from 1 occurrence, that is, no duplicate.
    # Only give the number of occurrences that have a penalty less than
    # infinity, including a 0.0 penalty (for e.g. a single, `1`, occurrence).
    # All penalties should be floating point numbers.
    penalties = {1 = 0.0, 2 = 0.0, 3 = 1.0, 4 = 5.0}
