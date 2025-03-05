from rest_framework_datatables.pagination import *

class CustomDatatablesPagination(DatatablesPageNumberPagination):
    """
    Paginator personnalisé pour DataTables avec les bonnes clés attendues.
    """
    

    def get_paginated_response(self, data):
        """
        Personnalise la réponse paginée pour inclure toutes les données attendues par DataTables.
        """
        request = self.request
        
        # Récupérer tous les paramètres envoyés par DataTables (draw, start, length, etc.)
        draw = int(request.query_params.get("draw", 1))
        start = int(request.query_params.get("start", 0))  # Index de départ pour la pagination
        length = int(request.query_params.get("length", 5))  # Nombre d'éléments par page
        search_value = request.query_params.get("search[value]", "")  # Valeur de recherche (si présente)
        order_column_index = request.query_params.get("order[1][column]", None)  # Index de colonne triée
        order_dir = request.query_params.get("order[1][dir]", "asc")  # Direction du tri
        
        # Obtenir le nom de la colonne à trier
        order_column = None
        if order_column_index is not None:
            try:
                order_column_index = int(order_column_index)
                order_column = request.query_params.get(f"columns[{order_column_index}][data]", None)
            except ValueError:
                order_column = None

        return Response({
            "draw": draw,  # Synchronisation avec DataTables
            "recordsTotal": self.page.paginator.count,  # Nombre total de lignes avant filtrage
            "recordsFiltered": self.page.paginator.count,  # Nombre après filtrage (peut être mis à jour si nécessaire)
            "start": start,  # Index de départ
            "length": length,  # Nombre d'éléments affichés
            "search_value": search_value,  # Terme recherché
            "order_column": order_column,  # Colonne triée
            "order_dir": order_dir,  # Direction de tri
            "data": data  # Liste des résultats paginés
        })

