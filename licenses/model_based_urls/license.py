from django.urls import path


from licenses.model_based_views import license as license_views


as_json_path = path(
    r'as_json/<int:pk>/',
    license_views.AsJSONView.as_view(),
    name='as_json',
)


as_json_for_humans_path = path(
    r'as_json_for_humans/<int:pk>/',
    license_views.AsJSONForHumansView.as_view(),
    name='as_json_for_humans',
)


get_path = path(
    r'get/',
    license_views.GetView.as_view(),
    name='get',
)


urlpatterns = (
    as_json_path,
    as_json_for_humans_path,

    get_path,
)
