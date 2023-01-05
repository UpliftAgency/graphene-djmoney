from graphene_django.debug.middleware import DjangoDebugMiddleware, DjangoDebugContext


class CustomDjangoDebugMiddleware(DjangoDebugMiddleware):
    def resolve(self, next, root, info, **args):
        context = info.context
        django_debug = getattr(context, "django_debug", None)
        if not django_debug:
            if context is None:
                raise Exception("DjangoDebug cannot be executed in None contexts")
            try:
                context.django_debug = DjangoDebugContext()
            except Exception:
                raise Exception(
                    "DjangoDebug need the context to be writable, context received: {}.".format(
                        context.__class__.__name__
                    )
                )
        if info.schema.get_type("DjangoDebug") == info.return_type:
            return context.django_debug.get_debug_promise()

        promise = next(root, info, **args)
        context.django_debug.add_promise(promise)
        return promise
