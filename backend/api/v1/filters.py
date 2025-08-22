from django_filters import rest_framework as filters
from django_filters.rest_framework import (BooleanFilter,
                                           DateTimeFromToRangeFilter)


class HomeWorkFilter(filters.FilterSet):
    """
    FilterSet for HomeWork model.
    """

    created_at = DateTimeFromToRangeFilter()
    isgraded = BooleanFilter(
        method='filter_by_is_graded'
    )
    issubmitted = BooleanFilter(
        method='filter_by_is_submitted'
    )

    def filter_by_is_graded(self, queryset, name, value):
        """
        Filters homeworks based on whether they have a grade.
        - `isgraded=true`: returns homeworks that have at least one graded submission.
        - `isgraded=false`: returns homeworks that have no graded submissions.
        """
        if value:
            return queryset.filter(submissions__grade__isnull=False).distinct()
        return queryset.exclude(submissions__grade__isnull=False)

    def filter_by_is_submitted(self, queryset, name, value):
        """
        Filters homeworks based on whether they have a submission.
        - `issubmitted=true`: returns homeworks that have at least one submission.
        - `issubmitted=false`: returns homeworks that have no submissions.
        """
        if value:
            return queryset.filter(submissions__isnull=False).distinct()
        return queryset.exclude(submissions__isnull=False)
