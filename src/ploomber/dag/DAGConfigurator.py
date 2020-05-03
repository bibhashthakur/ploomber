"""
As we started adding more features to DAG, I added a few more parameters to
the constructor, default values cover a lot of cases and most of the time
only a few parameters are actually modified. To prevent making the DAG API
unnecessarily complex, custom behavior will be provided via this object.

This is based in the essence pattern by by Andy Carlson
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.81.1898&rep=rep1&type=pdf
"""
from copy import copy
from ploomber.dag.DAG import DAG
from ploomber.dag.DAGConfiguration import DAGConfiguration


class DAGConfigurator:
    """An object to customize DAG behavior

    Note: this API is experimental an subject to change

    To keep the DAG API clean, only the most important parameters are included
    in the constructor, the rest are accesible via a DAGConfigurator object

    Available parameters:

    outdated_by_code: whether source code differences make a task outdated
    cache_rendered_status: keep results from dag.render() whenever are needed
    again (e.g. when calling dag.build()) or compute it again every time.

    cache_rendered_status: If True, once the DAG is rendered, subsequent calls
    to render will not do anything (rendering is implicitely called in build,
    plot, status), otherwise it will always render again.

    Examples
    --------
    >>> from ploomber import DAGConfigurator
    >>> configurator = DAGConfigurator()
    >>> configurator.param.outdated_by_code = True
    >>> configurator.param.cache_rendered_status = False
    >>> dag = configurator.create()
    """
    def __init__(self, d=None):
        if d:
            self._param = DAGConfiguration.from_dict(d)
        else:
            self._param = DAGConfiguration()

    @property
    def param(self):
        return self._param

    def create(self, *args, **kwargs):
        """Return a DAG with the given parameters

        *args, **kwargs
            Parameters to pass to the DAG constructor
        """
        dag = DAG(*args, **kwargs)
        dag._param = copy(self.param)
        return dag

    def __setattr__(self, key, value):
        if key != '_param':
            raise AttributeError('Cannot assign attributes to DAGConfigurator,'
                                 ' use configurator.param.param_name = value')
        super().__setattr__(key, value)
