from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import ugettext as _

from django_chunk_upload.settings import EXPIRATION_DELTA
from django_chunk_upload.models import ChunkUpload
from django_chunk_upload.constants import UPLOADING, COMPLETE

prompt_msg = _(u'Do you want to delete {obj}?')


class Command(BaseCommand):
    # Has to be a ChunkUpload subclass
    model = ChunkUpload

    help = 'Deletes chunk uploads that have already expired.'

    option_list = BaseCommand.option_list + (
        make_option('--interactive',
                    action='store_true',
                    dest='interactive',
                    default=False,
                    help='Prompt confirmation before each deletion.'),
    )

    def handle(self, *args, **options):
        interactive = options.get('interactive')

        count = {UPLOADING: 0, COMPLETE: 0}
        qs = self.model.objects.all()
        qs = qs.filter(created_on__lt=(timezone.now() - EXPIRATION_DELTA))

        for chunk_upload in qs:
            if interactive:
                prompt = prompt_msg.format(obj=chunk_upload) + u' (y/n): '
                answer = input(prompt).lower()
                while answer not in ('y', 'n'):
                    answer = input(prompt).lower()
                if answer == 'n':
                    continue

            count[chunk_upload.status] += 1
            # Deleting objects individually to call delete method explicitly
            chunk_upload.delete()

        print('%i complete uploads were deleted.' % count[COMPLETE])
        print('%i incomplete uploads were deleted.' % count[UPLOADING])
