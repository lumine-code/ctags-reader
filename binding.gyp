{
  'targets': [
    {
      'target_name': 'ctags',
      'include_dirs': [ '<!(node -p "require(\'node-addon-api\').include_dir")' ],
      # An AsyncWorker that completes while the environment is tearing down
      # (window reload, app quit) cannot call back into JS. Without these two
      # defines node-addon-api escalates that to napi_fatal_error and aborts the
      # process. The graceful path in Error::ThrowAsJavaScriptException needs
      # NODE_API_SWALLOW_UNTHROWABLE_EXCEPTIONS *and* NAPI_VERSION >= 10, since
      # below 10 it expects napi_pending_exception instead of napi_cannot_run_js
      # and never matches. napi_build_version is 10 on Node 22+ and Electron 43.
      'defines': [
        'NAPI_VERSION=<(napi_build_version)',
        'NODE_API_SWALLOW_UNTHROWABLE_EXCEPTIONS',
      ],
      'cflags!': [ '-fno-exceptions' ],
      'cflags_cc!': [ '-fno-exceptions' ],
      'xcode_settings': {
        'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
        'CLANG_CXX_LIBRARY': 'libc++',
      },
      'msvs_settings': {
        'VCCLCompilerTool': { 'ExceptionHandling': 1 },
      },
      'sources': [
        'src/readtags.c',
        'src/tags.cc',
        'src/tag-finder.cc',
        'src/tag-reader.cc'
      ],
      'conditions': [
        ['OS=="win"', {
          'msvs_disabled_warnings': [
            4267,  # conversion from 'size_t' to 'int', possible loss of data
            4530,  # C++ exception handler used, but unwind semantics are not enabled
            4506,  # no definition for inline function
          ],
        }],
      ],
    }
  ]
}
