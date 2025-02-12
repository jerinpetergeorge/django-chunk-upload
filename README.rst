django-chunk-upload
=====================

This simple django app enables users to upload large files to Django in multiple chunks, with the ability to resume if the upload is interrupted.

The most of the code base belongs to `django-chunked-upload <https://github.com/juliomalegria/django-chunked-upload>`__ of `juliomalegria <https://github.com/juliomalegria/>`__ and I would like to thank him for this awesome package.

This app is intented to work with `JQuery-File-Upload <https://github.com/blueimp/jQuery-File-Upload>`__ by `Sebastian Tschan <https://blueimp.net>`__ (`documentation <https://github.com/blueimp/jQuery-File-Upload/wiki>`__).

License: `MIT-Zero <https://romanrm.net/mit-zero>`__.

Demo
----

If you want to see a very simple Django demo project using this module, please take a look at `django-chunk-upload-demo <https://github.com/jerinpetergeorge/django-chunk-upload-demo>`__.

Installation
------------

Install via pip:

::

    pip install django-chunk-upload

And then add it to your Django ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = (
        # ...
        'django_chunk_upload',
    )

Typical usage
-------------

1. An initial POST request is sent to the url linked to ``ChunkUploadView`` (or any subclass) with the first chunk of the file. The name of the chunk file can be overriden in the view (class attribute ``field_name``). Example:

::

    {"my_file": <File>}

2. In return, server with response with the ``upload_id``, the current ``offset`` and the when will the upload expire (``expires``). Example:

::

    {
        "upload_id": "5230ec1f59d1485d9d7974b853802e31",
        "offset": 10000,
        "expires": "2013-07-18T17:56:22.186Z"
    }

3. Repeatedly POST subsequent chunks using the ``upload_id`` to identify the upload  to the url linked to ``ChunkUploadView`` (or any subclass). Example:

::

    {
        "upload_id": "5230ec1f59d1485d9d7974b853802e31",
        "my_file": <File>
    }

4. Server will continue responding with the ``upload_id``, the current ``offset`` and the expiration date (``expires``).

5. Finally, when upload is completed, a POST request is sent to the url linked to ``ChunkUploadCompleteView`` (or any subclass). This request must include the ``upload_id`` and the ``md5`` checksum (hex). Example:

::

    {
        "upload_id": "5230ec1f59d1485d9d7974b853802e31",
        "md5": "fc3ff98e8c6a0d3087d515c0473f8677"
    }

6. If everything is OK, server will response with status code 200 and the data returned in the method ``get_response_data`` (if any).

Possible error responses:
~~~~~~~~~~~~~~~~~~~~~~~~~

* User is not authenticated. Server responds 403 (Forbidden).
* Upload has expired. Server responds 410 (Gone).
* ``upload_id`` does not match any upload. Server responds 404 (Not found).
* No chunk file is found in the indicated key. Server responds 400 (Bad request).
* Request does not contain ``Content-Range`` header. Server responds 400 (Bad request).
* Size of file exceeds limit (if specified).  Server responds 400 (Bad request).
* Offsets does not match.  Server responds 400 (Bad request).
* ``md5`` checksums does not match. Server responds 400 (Bad request).

Settings
--------

Add any of these variables into your project settings to override them.

``DJANGO_CHUNK_UPLOAD_EXPIRATION_DELTA``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* How long after creation the upload will expire.
* Default: ``datetime.timedelta(days=1)``

``DJANGO_CHUNK_UPLOAD_PATH``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Path where uploading files will be stored until completion.
* Default: ``'chunk_uploads/%Y/%m/%d'``

``DJANGO_CHUNK_UPLOAD_TO``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `upload_to` to be used in the Model's FileField.
* Default: ``DJANGO_CHUNK_UPLOAD_PATH + '/{{ instance.upload_id }}.part'``

``DJANGO_CHUNK_UPLOAD_STORAGE_CLASS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Storage system (should be a class).
* Default: ``None`` (use default storage system)

``DJANGO_CHUNK_UPLOAD_USE_TEMP_STORAGE``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Activates temporary file storage. Useful for AWS S3.
* Default: ``False`` (use default storage system or ``CHUNKED_UPLOAD_STORAGE_CLASS``)

``DJANGO_CHUNK_UPLOAD_ABSTRACT_MODEL``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Boolean that defines if the ``ChunkUpload`` model will be abstract or not (`what does abstract model mean? <https://docs.djangoproject.com/en/1.4/ref/models/options/#abstract>`__).
* Default: ``True``

``DJANGO_CHUNK_UPLOAD_NULL_USER``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Boolean that defines whether the "user" field of ``ChunkUpload`` model can be ``NULL`` or not
* Default: ``True``

``DJANGO_CHUNK_UPLOAD_ENCODER``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Function used to encode response data. Receives a dict and returns a string.
* Default: ``DjangoJSONEncoder().encode``

``DJANGO_CHUNK_UPLOAD_CONTENT_TYPE``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Content-Type for the response data.
* Default: ``'application/json'``

``DJANGO_CHUNK_UPLOAD_MAX_BYTES``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Max amount of data (in bytes) that can be uploaded. ``None`` means no limit.
* Default: ``None``

Support
-------

If you find any bug or you want to propose a new feature, please use the `issues tracker <https://github.com/jerinpetergeorge/django-chunk-upload/issues>`__. I'll be happy to help you! :-)
