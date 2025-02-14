from rest_framework_datatables.pagination import *

class CustomDatatablesPagination(DatatablesPageNumberPagination):
    """
    Paginator personnalisé pour DataTables avec les bonnes clés attendues.
    """

    def get_paginated_response(self, data):
        """
        Personnalise la réponse paginée pour inclure les bonnes clés attendues
        par DataTables : recordsTotal, recordsFiltered et data.
        """
        response = super().get_paginated_response(data)

        # Adapter les clés pour correspondre aux attentes de DataTables
        return Response({
            "recordsTotal": self.page.paginator.count,  # Nombre total d'éléments
            "recordsFiltered": self.page.paginator.count,  # Filtrage non géré ici, on met count
            "data": response.data["results"]  # Remplace "results" par "data"
        })
