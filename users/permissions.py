from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin()

class IsEditorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_editor()

class IsReaderUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_reader()

class CanAccessNews(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Se a notícia é pública, qualquer usuário pode acessar
        if obj.access_type == 'PUBLIC':
            return True
        
        # Se é conteúdo PRO, verifica se o usuário tem acesso
        if obj.access_type == 'PRO':
            # Se o usuário não tem plano PRO, não tem acesso
            if not request.user.has_pro_access():
                return False
            
            # Se a notícia tem vertical, verifica se o usuário tem acesso a ela
            if obj.vertical:
                return request.user.can_access_vertical(obj.vertical)
            
            # Se não tem vertical, qualquer usuário PRO tem acesso
            return True
        
        return False 