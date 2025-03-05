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
        request = self.request


        # Adapter les clés pour correspondre aux attentes de DataTables
        return Response({
            **request.query_params,  # Ajoute TOUS les paramètres reçus par DataTables
            "recordsTotal": self.page.paginator.count,  # Nombre total d'éléments
            "recordsFiltered": self.page.paginator.count,  # Filtrage non géré ici
            "data": data  # La liste paginée des résultats
        })
