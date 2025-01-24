import matplotlib.pyplot as plt
import astropy.units as u
import sunpy.data.sample
import sunpy.map
import sunkit_image.radial as radial
from sunkit_image.utils import equally_spaced_bins

###########################################################################
# Load the sample AIA 171 image.

aia_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)

###########################################################################
# Create radial bin edges and apply the NRGF, FNRGF, and RHEF filters.

viggy = 1.5 * u.R_sun

radial_bin_edges = equally_spaced_bins(0, 2, aia_map.data.shape[0] // 1)
radial_bin_edges *= u.R_sun

base_nrgf = radial.nrgf(
    aia_map,
    radial_bin_edges=radial_bin_edges,
    application_radius=1.0 * u.R_sun,
    progress=True,
    vignette=viggy,
)


order = 10
attenuation_coefficients = radial.set_attenuation_coefficients(order)


base_fnrgf = radial.fnrgf(
    aia_map,
    radial_bin_edges,
    order,
    attenuation_coefficients,
    application_radius=1.0 * u.R_sun,
    progress=True,
    vignette=viggy,
)

base_rhef = radial.rhef(
    aia_map,
    radial_bin_edges=radial_bin_edges,
    application_radius=0 * u.R_sun,
    progress=True,
    vignette=viggy,
    method="scipy",
)

###########################################################################
# Create subplots that share both x and y axes.

fig, axs = plt.subplots(2, 2, figsize=(8, 8), sharex="all", sharey="all", subplot_kw={"projection": aia_map})

###########################################################################
# Plot the original map and the filtered maps on the shared axes.

aia_map.plot(axes=axs[0, 0], clip_interval=(1, 99.99) * u.percent)
aia_map.plot(axes=axs[0, 1], clip_interval=(1, 99.99) * u.percent)
aia_map.plot(axes=axs[1, 0], clip_interval=(1, 99.99) * u.percent)
axs[0, 0].set_title("Original AIA 171")

base_nrgf.plot(axes=axs[0, 1], clip_interval=(1, 99.99) * u.percent)
axs[0, 1].set_title("NRGF")

base_fnrgf.plot(axes=axs[1, 0], clip_interval=(1, 99.99) * u.percent)
axs[1, 0].set_title("FNRGF")

base_rhef.plot(axes=axs[1, 1], clip_interval=(1, 99.99) * u.percent)
axs[1, 1].set_title("RHEF")

###########################################################################
# Set facecolor to black for all axes and hide tick labels for better visibility.

for ax in axs.flat:
    ax.set_facecolor("k")

axs[0, 0].coords[0].set_ticklabel_visible(False)
axs[0, 1].coords[0].set_ticklabel_visible(False)
axs[0, 1].coords[1].set_ticklabel_visible(False)
axs[1, 1].coords[1].set_ticklabel_visible(False)


fig.tight_layout()
plt.savefig("/Users/cgilbert/vscode/sunback_data/renders/Single_Test/quadFirst.pdf", dpi=300)
plt.show()
