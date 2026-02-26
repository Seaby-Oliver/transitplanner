import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np

def plot_lightcurve(obstime, flux, info, title="Light Curve"):
    """
    This function visualises the simulated transit flux as a function of
    observation time. It also overlays error bars at key transit phases,
    specifically ingress, mid transit and egress.

    Marker indices and photometric uncertainty are provided through the
    info dictionary, which is produced by the light curve simulation stage.

    Parameters
    
    obstime : array-like
        Observation time array in hours from start of transit.
    flux : array-like
        Relative flux values for the lightcurve.
    info : dict
        Dictionary containing lightcurve metadata, including markers and errors.
    title : str, optional
        Plot title. Default is "Light Curve".

    
      it  Displays and saves the plot.
    """
    
    ingress,t2, indepth,t3, egress = info["markers"]
    error = info["error"]

    fig, ax = plt.subplots()
    ax.plot(obstime,flux) #Transit Curve
    ax.errorbar(obstime[[ingress,t2,indepth,t3,egress]],flux[[ingress,t2,indepth,t3,egress]],error,fmt='o',c='r',zorder=3)
    ax.scatter([obstime[t2],obstime[t3]],[flux[t2],flux[t3]],c='r',zorder=3)
    ymin, ymax = ax.get_ylim()

    lower = np.min(flux[[ingress, t2, indepth, t3, egress]] - error)
    upper = np.max(flux[[ingress, t2, indepth, t3, egress]] + error)
    ax.set_ylim(min(ymin, lower), max(ymax, upper))

    # Create transform: x in data coords, y in axis coords
    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    y_ing_ax = (flux[ingress] - ymin) / (ymax - ymin)
    y_egr_ax = (flux[egress] - ymin) / (ymax - ymin)
    y_t2_ax = (flux[ingress+t2] - ymin) / (ymax - ymin)
    y_t3_ax = (flux[indepth+t3]- ymin) / (ymax - ymin)

    # Draw vertical lines from bottom of plot to contact points
    ax.plot([obstime[ingress], obstime[ingress]],
            [0, y_ing_ax],
            transform=trans,
            linestyle='dashed',
            c='b')
    ax.plot([obstime[egress], obstime[egress]],
            [0, y_egr_ax],
            transform=trans,
            linestyle='dashed',
            c='b')
    ax.plot([obstime[t2],obstime[t2]],
            [0,y_t2_ax],
            transform=trans,
            linestyle='--',
            c='b')
    ax.plot([obstime[t3],obstime[t3]],
            [0,y_t3_ax],
            transform=trans,
            linestyle='--',
            c='b')
    ax.plot([obstime[10],obstime[10]],
            [(flux[indepth-5]- ymin) / (ymax - ymin),(flux[10]- ymin) / (ymax - ymin)],
            transform=trans,
            c='black')
    ax.plot(obstime[10],flux[10],marker='_',c='black'),ax.plot(obstime[10],flux[indepth],marker='_',c='black')
    plt.xlabel('Observation Time (Hours)'),plt.ylabel('Relative Flux')
    plt.title(title)

    #Annotations
    #T1
    ax.annotate("$T_1$",(obstime[ingress], flux[ingress]),xytext=(5,2),textcoords='offset points')
    #T2
    ax.annotate("$T_2$",(obstime[t2], flux[t2]), xytext=(5,2), textcoords='offset points')
    #T3
    ax.annotate("$T_3$",(obstime[t3], flux[t3]), xytext=(-15,2),textcoords='offset points')
    #T4
    ax.annotate("$T_4$",(obstime[egress], flux[egress]),xytext=(-15,2),textcoords='offset points')
    #Midpoint T0
    ax.annotate('$T_0$',(obstime[indepth],flux[indepth]),xytext=(2,5),textcoords='offset points')
    #Transit depth delta
    ax.annotate(r'$\delta$',(obstime[10],(flux[10]+flux[indepth])/2),xytext=(-10,0),textcoords='offset points')
    
    plt.savefig('lightcurve.png',dpi=150,bbox_inches='tight')
    plt.show

